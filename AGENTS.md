# AGENTS.md — 本仓库工作约定

> 供在此仓库工作的编程智能体（Codex / ZCode / DeepSeek harness / Claude Code / Cursor 等）阅读。人写的完整维护手册见 [MAINTENANCE.md](MAINTENANCE.md)。

## 这是什么仓库
「Codex Task Mastery」：一套任务总控技能包（`skills/`，10 个技能）+ 福建代账智能体项目开展提示词 + 研究底稿。技能遵循 [Agent Skills 官方规范](https://agentskills.io/specification)。

## 布局
- `skills/` — 技能源码（**唯一可编辑副本**；不要直接改 `~/.codex/skills/` 里的安装副本）
- `福建代账智能体-*.md`、`分段粘贴/` — 项目开展提示词；**执行提示词是唯一事实源**，精简版与分段版由它派生
- `项目开展提示词-通用骨架.md` — 跨智能体开工提示词写法
- `_research/` — 外部研究底稿与对标报告（只读参考）
- `install-skills.ps1` / `lint-skills.py` — 安装同步与规范检查工具
- `.omx/`、`output/` — 运行时状态与产物，不入库

## 验证命令（改动后必须跑）
```bash
python lint-skills.py                                                    # 技能规范检查
powershell -ExecutionPolicy Bypass -File install-skills.ps1 -Mode check  # 源与安装端一致
```

## 约定
- 改 `skills/` 后：lint → commit → `install-skills.ps1`（安装）→ 新会话生效。
- 新增技能必须同时登记三处：README 技能表、`codex-mastery` 路由表（流程技能）、CHANGELOG。
- `分段粘贴/` 不手改；执行提示词更新后重新切分，并保证「8 段按序拼接 = 全文」（校验命令见 MAINTENANCE.md）。
- 遵循本仓库技能包自身的纪律：证据收口（没跑的验证不说"完成"）、范围纪律（不顺手重构）、简单任务不过度流程化。
- 所有变更记录进 CHANGELOG.md；仓库版本用 semver。
