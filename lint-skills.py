#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""lint-skills.py — 按 Agent Skills 官方规范（agentskills.io/specification）校验 skills/ 目录，
并做仓库「登记一致性」检查（skills/ ↔ README 技能表 ↔ codex-mastery 路由 ↔ MAINTENANCE 触发用例）。

检查项：
  ERROR（存在即退出码 1）
    - 缺 SKILL.md / frontmatter 无法解析
    - name 缺失、不符合命名规则（1-64 位小写字母数字+单连字符，不得以连字符开头/结尾/连续）
    - name 与目录名不一致
    - description 缺失或超过 1024 字符
    - SKILL.md 超过 500 行
    - 正文中引用的 references/scripts/assets 文件不存在
    - 登记一致性：技能漏登记进 README 技能表 / MAINTENANCE 触发用例表 / codex-mastery；
      登记表引用了不存在的技能名
  WARN（不影响退出码）
    - references/scripts/assets 下存在未被 SKILL.md 引用的文件（孤儿文件）

用法：
    python lint-skills.py                    # 规范 + 登记一致性检查
    python lint-skills.py --no-registry      # 只做规范检查
    python lint-skills.py --root <dir>       # 检查指定技能根目录
    python lint-skills.py --strict           # 把 WARN 也当错误（退出码 1）
    python lint-skills.py --self-test        # 校验器自测试（内置正反样本，验证器自身的回归测试）
"""
import argparse
import re
import sys
import tempfile
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DESC_MAX = 1024
LINE_MAX = 500
REF_RE = re.compile(r"(?:references|scripts|assets)/[A-Za-z0-9\-_./]+")
TOKEN_RE = re.compile(r"`([a-z][a-z0-9-]*)`")


def lint_skill(skill_dir: Path):
    errors, warns = [], []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return ["缺 SKILL.md"], []

    text = skill_md.read_text(encoding="utf-8-sig")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return ["frontmatter 缺失或无法解析（应以 --- 开始和结束）"], []

    fm = m.group(1)
    name_m = re.search(r"^name:\s*(\S+)\s*$", fm, re.M)
    desc_m = re.search(r"^description:\s*(.+)$", fm, re.M)

    name = name_m.group(1) if name_m else None
    if not name:
        errors.append("name 缺失")
    else:
        if not (1 <= len(name) <= 64) or not NAME_RE.match(name):
            errors.append(f"name 不符合规范：{name!r}（需 1-64 位小写字母数字+单连字符）")
        if name != skill_dir.name:
            errors.append(f"name ({name!r}) 与目录名 ({skill_dir.name!r}) 不一致")

    if not desc_m:
        errors.append("description 缺失")
    else:
        dlen = len(desc_m.group(1).strip())
        if dlen == 0:
            errors.append("description 为空")
        elif dlen > DESC_MAX:
            errors.append(f"description {dlen} 字符，超过上限 {DESC_MAX}")

    n_lines = text.count("\n") + 1
    if n_lines > LINE_MAX:
        errors.append(f"SKILL.md {n_lines} 行，超过建议上限 {LINE_MAX} 行")

    for ref in sorted(set(REF_RE.findall(text))):
        if not (skill_dir / ref).exists():
            errors.append(f"引用的文件不存在：{ref}")

    for sub in ("references", "scripts", "assets"):
        sub_dir = skill_dir / sub
        if not sub_dir.is_dir():
            continue
        for f in sorted(sub_dir.rglob("*")):
            if f.is_file():
                rel = f.relative_to(skill_dir).as_posix()
                if rel not in text:
                    warns.append(f"未被 SKILL.md 引用：{rel}")

    return errors, warns


def extract_section(text: str, keyword: str) -> str:
    """取 markdown 中标题含 keyword 的 '## ' 小节（到下一个 '## ' 为止，不含标题行）。"""
    buf, on = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            if on:
                break
            on = keyword in line
            continue
        if on:
            buf.append(line)
    return "\n".join(buf)


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def check_registry(root: Path, skill_names, errors):
    """登记一致性：skills/ 目录与三处登记（README 技能表 / MAINTENANCE 触发用例 / codex-mastery）互相校验。

    前向：每个技能目录都必须出现在三处登记中（codex-mastery 只查正文，不看 frontmatter，
    避免仅凭 description 里的名字蒙混过关）。
    反向：README 技能表第一列与 codex-mastery 路由表小节里的反引号技能名，都必须是真实存在的技能目录。
    """
    names = set(skill_names)
    repo = root.parent
    readme = repo / "README.md"
    maint = repo / "MAINTENANCE.md"
    router = repo / "skills" / "codex-mastery" / "SKILL.md"

    for label, path, keyword in (
        ("README 技能表", readme, "包含的技能"),
        ("MAINTENANCE 触发用例表", maint, "触发自测"),
    ):
        if not path.is_file():
            errors.append(f"登记一致性：找不到 {path.name}（--root 应指向仓库内 skills/ 目录；或用 --no-registry 跳过）")
            continue
        sec = extract_section(path.read_text(encoding="utf-8-sig"), keyword)
        for n in sorted(names):
            if not re.search(rf"`?{re.escape(n)}`?", sec):
                errors.append(f"登记一致性：技能 {n} 未登记进 {label}")

    if not router.is_file():
        errors.append("登记一致性：找不到 skills/codex-mastery/SKILL.md（路由表）")
        return
    router_text = router.read_text(encoding="utf-8-sig")
    router_body = strip_frontmatter(router_text)
    for n in sorted(names):
        if n == "codex-mastery":
            continue  # 路由器自身不是被路由对象，不要求出现在路由表里
        if not re.search(rf"`?{re.escape(n)}`?", router_body):
            errors.append(f"登记一致性：技能 {n} 未出现在 codex-mastery（路由表或领域技能注记）")
    # 反向只查表格行：路由目标都写在表里；散文里的反引号词（如 `description`）不是路由对象
    for line in extract_section(router_body, "路由表").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        for tok in TOKEN_RE.findall(line):
            if tok not in names:
                errors.append(f"登记一致性：codex-mastery 路由表引用了不存在的技能：{tok}")

    if readme.is_file():
        for row in extract_section(readme.read_text(encoding="utf-8-sig"), "包含的技能").splitlines():
            if row.startswith("| `") and row.count("`") >= 2:
                tok = row.split("`")[1]
                if tok not in names:
                    errors.append(f"登记一致性：README 技能表登记了不存在的技能：{tok}")


def self_test() -> int:
    """校验器自测试：内置正反样本，验证 lint_skill / check_registry 的检查逻辑本身没有回归。"""
    failures = []

    def expect(label, got_errors, got_warns, want_err=None, want_warn=None, want_clean=False):
        if want_clean and not got_errors and not got_warns:
            return
        if want_err and any(want_err in e for e in got_errors):
            return
        if want_warn and any(want_warn in w for w in got_warns):
            return
        wanted = "通过（无错误无警告）" if want_clean else (f"错误含 {want_err!r}" if want_err else f"警告含 {want_warn!r}")
        failures.append(f"[{label}] 未命中期望（{wanted}）；实际错误={got_errors}，警告={got_warns}")

    def make_skill(d: Path, name: str, fm_lines, body="正文\n"):
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text("---\n" + "".join(l + "\n" for l in fm_lines) + "---\n" + body, encoding="utf-8")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        # 正样本：合规技能应完全通过
        make_skill(root / "good-skill", "good-skill", ["name: good-skill", "description: A valid test skill."])
        e, w = lint_skill(root / "good-skill")
        expect("正样本", e, w, want_clean=True)

        # 反样本：逐类错误必须被捕获
        (root / "no-skillmd").mkdir()
        e, w = lint_skill(root / "no-skillmd")
        expect("缺 SKILL.md", e, w, want_err="缺 SKILL.md")

        d = root / "bad-fm"; d.mkdir()
        (d / "SKILL.md").write_text("没有 frontmatter 的正文\n", encoding="utf-8")
        e, w = lint_skill(d)
        expect("frontmatter 缺失", e, w, want_err="frontmatter 缺失")

        make_skill(root / "name-mismatch", "beta", ["name: beta", "description: x"])
        e, w = lint_skill(root / "name-mismatch")
        expect("name 与目录名不一致", e, w, want_err="与目录名")

        make_skill(root / "name-bad", "Bad_Name", ["name: Bad_Name", "description: x"])
        e, w = lint_skill(root / "name-bad")
        expect("name 不合规", e, w, want_err="name 不符合规范")

        make_skill(root / "desc-missing", "desc-missing", ["name: desc-missing"])
        e, w = lint_skill(root / "desc-missing")
        expect("description 缺失", e, w, want_err="description 缺失")

        make_skill(root / "desc-long", "desc-long", ["name: desc-long", "description: " + "x" * 1100])
        e, w = lint_skill(root / "desc-long")
        expect("description 超长", e, w, want_err="超过上限")

        make_skill(root / "too-long", "too-long", ["name: too-long", "description: x"], body="\n" * 600)
        e, w = lint_skill(root / "too-long")
        expect("超过行数上限", e, w, want_err="超过建议上限")

        make_skill(root / "ref-missing", "ref-missing",
                   ["name: ref-missing", "description: x"], body="见 references/ghost.md\n")
        e, w = lint_skill(root / "ref-missing")
        expect("引用文件不存在", e, w, want_err="引用的文件不存在")

        d = root / "orphan"
        make_skill(d, "orphan", ["name: orphan", "description: x"])
        (d / "references").mkdir()
        (d / "references" / "extra.md").write_text("孤儿文件\n", encoding="utf-8")
        e, w = lint_skill(d)
        expect("孤儿文件告警", e, w, want_warn="未被 SKILL.md 引用")

    with tempfile.TemporaryDirectory() as td:
        repo = Path(td)
        sk = repo / "skills"
        make_skill(sk / "alpha", "alpha", ["name: alpha", "description: Skill alpha."])
        make_skill(sk / "beta", "beta", ["name: beta", "description: Skill beta."])
        cm = sk / "codex-mastery"
        cm.mkdir(parents=True, exist_ok=True)
        (cm / "SKILL.md").write_text(
            "---\nname: codex-mastery\ndescription: router.\n---\n\n"
            "## 路由表\n| 情况 | 调用 |\n|---|---|\n| x | `alpha` |\n\n"
            "> 本路由只分发流程技能，领域技能按各自 `description` 触发加载。\n", encoding="utf-8")
        (repo / "MAINTENANCE.md").write_text(
            "# M\n\n## 5. 触发自测用例\n| 话术 | 预期触发 |\n|---|---|\n| a | alpha |\n| b | beta |\n", encoding="utf-8")
        (repo / "README.md").write_text(
            "# R\n\n## 包含的技能\n| 技能 | 作用 |\n|---|---|\n| `alpha` | x |\n| `ghost` | y |\n", encoding="utf-8")

        errs = []
        check_registry(sk, {"alpha", "beta"}, errs)
        expect("登记一致性：README 漏登记", errs, [], want_err="技能 beta 未登记进 README 技能表")
        expect("登记一致性：codex-mastery 漏登记", errs, [], want_err="技能 beta 未出现在 codex-mastery")
        expect("登记一致性：README 未知技能", errs, [], want_err="README 技能表登记了不存在的技能：ghost")
        # beta 在路由表正文里未以反引号出现，不应触发反向检查；MAINTENANCE 应全部通过
        if any("MAINTENANCE" in e for e in errs):
            failures.append(f"[登记一致性：MAINTENANCE 应通过] 实际：{errs}")
        # 散文里的反引号词（如 `description`）不是路由对象，不得触发反向检查
        if any("不存在的技能：description" in e for e in errs):
            failures.append(f"[登记一致性：散文反引号误报] 实际：{errs}")

    if failures:
        print("自测试未通过：")
        for f in failures:
            print(f"    FAIL: {f}")
        return 1
    print("自测试通过：正样本通过 + 9 类技能错误/告警全捕获 + 登记一致性 3 类错误全捕获")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Agent Skills 规范与登记一致性校验器")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent / "skills"),
                    help="待检查的技能根目录（默认本仓库 skills/）")
    ap.add_argument("--strict", action="store_true", help="把 WARN 也当错误")
    ap.add_argument("--no-registry", action="store_true", help="跳过登记一致性检查")
    ap.add_argument("--self-test", action="store_true", help="运行校验器自测试（忽略 --root）")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())

    root = Path(args.root)
    if not root.is_dir():
        print(f"[错误] 目录不存在：{root}")
        sys.exit(2)

    skill_dirs = sorted(d for d in root.iterdir() if d.is_dir())
    if not skill_dirs:
        print(f"[错误] 目录下没有技能文件夹：{root}")
        sys.exit(2)

    total_err = total_warn = 0
    for d in skill_dirs:
        errors, warns = lint_skill(d)
        status = "OK " if not errors else "FAIL"
        print(f"[{status}] {d.name}")
        for e in errors:
            print(f"    ERROR: {e}")
        for w in warns:
            print(f"    WARN : {w}")
        total_err += len(errors)
        total_warn += len(warns)

    if not args.no_registry:
        print("-" * 50)
        print("[REGISTRY] 登记一致性（skills/ - README - codex-mastery - MAINTENANCE）")
        registry_errors = []
        check_registry(root, [d.name for d in skill_dirs], registry_errors)
        for e in registry_errors:
            print(f"    ERROR: {e}")
        total_err += len(registry_errors)

    print("-" * 50)
    print(f"共 {len(skill_dirs)} 个技能：{total_err} 个错误，{total_warn} 个警告")
    print("结果：" + ("通过" if total_err == 0 and not (args.strict and total_warn) else "未通过"))
    sys.exit(0 if total_err == 0 and not (args.strict and total_warn) else 1)


if __name__ == "__main__":
    main()
