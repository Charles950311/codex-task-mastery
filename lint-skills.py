#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""lint-skills.py — 按 Agent Skills 官方规范（agentskills.io/specification）校验 skills/ 目录。

检查项：
  ERROR（存在即退出码 1）
    - 缺 SKILL.md / frontmatter 无法解析
    - name 缺失、不符合命名规则（1-64 位小写字母数字+单连字符，不得以连字符开头/结尾/连续）
    - name 与目录名不一致
    - description 缺失或超过 1024 字符
    - SKILL.md 超过 500 行
    - 正文中引用的 references/scripts/assets 文件不存在
  WARN（不影响退出码）
    - references/scripts/assets 下存在未被 SKILL.md 引用的文件（孤儿文件）

用法：
    python lint-skills.py                # 检查本仓库 skills/
    python lint-skills.py --root <dir>   # 检查指定目录
    python lint-skills.py --strict       # 把 WARN 也当错误（退出码 1）
"""
import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DESC_MAX = 1024
LINE_MAX = 500
REF_RE = re.compile(r"(?:references|scripts|assets)/[A-Za-z0-9\-_./]+")


def lint_skill(skill_dir: Path):
    errors, warns = [], []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"缺 SKILL.md"], []

    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return [f"frontmatter 缺失或无法解析（应以 --- 开始和结束）"], []

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


def main():
    ap = argparse.ArgumentParser(description="Agent Skills 规范校验器")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent / "skills"),
                    help="待检查的技能根目录（默认本仓库 skills/）")
    ap.add_argument("--strict", action="store_true", help="把 WARN 也当错误")
    args = ap.parse_args()

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

    failed = total_err if not args.strict else total_err + total_warn
    print("-" * 50)
    print(f"共 {len(skill_dirs)} 个技能：{total_err} 个错误，{total_warn} 个警告")
    print("结果：" + ("通过" if failed == 0 else "未通过"))
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
