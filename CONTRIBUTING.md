# CONTRIBUTING — 贡献指南

欢迎为本技能包贡献。本仓库有自己的维护纪律，先读 [AGENTS.md](AGENTS.md)（仓库约定）与 [MAINTENANCE.md](MAINTENANCE.md)（维护手册）；本文件只讲外部贡献者需要知道的部分。

## 可以贡献什么
- **改进现有技能**：`skills/` 下 10 个技能的 `SKILL.md` / `references/` / `scripts/`。
- **新增技能**：走 MAINTENANCE.md 清单 B 的完整流程。
- **工具与校验**：`lint-skills.py`、`install-skills.ps1`。
- **文档修正**：README / MAINTENANCE / 本文件。

## 请勿改动
- `_research/` — 研究底稿为只读参考。
- 福建代账业务提示词在独立私有仓 `fj-daizhang-prompts`，不在本仓贡献范围。

## 改动前后的验证（必做）
```bash
python lint-skills.py                                                    # 技能规范检查，退出码非 0 即未通过
powershell -ExecutionPolicy Bypass -File install-skills.ps1 -Mode check  # 源与安装端一致（Windows）
./install-skills.sh --mode check                                         # 源与安装端一致（macOS/Linux/Git Bash）
```

## 新增技能的最小流程
1. 目录名 = 技能名（小写字母数字 + 单连字符），建 `skills/<name>/SKILL.md`。
2. frontmatter 必填 `name` + `description`（≤1024 字符，写清「做什么 + 何时用 + 何时不用」，建议中英双语触发词）。
3. 正文 <500 行；长内容进 `references/`，可复算逻辑进 `scripts/`（优先纯标准库，明确依赖）。
4. 同步登记三处：README 技能表、`codex-mastery` 路由表（流程技能）、CHANGELOG。
5. 在 MAINTENANCE.md 第 5 节补 2-3 条触发自测用例。

## 提交约定
- 一次提交对应一个可说明的主题，不混入无关改动。
- 所有变更记入 CHANGELOG.md；版本号由维护者发版时统一确定，PR 中写清变更内容即可。

## 第三方内容红线
- **禁止**向仓库新增第三方图片、音频、或逐字拷贝的文档。
- 引用外部项目：给链接与出处即可；确需引入内容片段时，源必须有明确许可证，并在 PR 中说明，由维护者登记进 [NOTICE.md](NOTICE.md)。

## 许可证
提交贡献即表示同意该贡献按仓库 [MIT](LICENSE) 许可证发布。
