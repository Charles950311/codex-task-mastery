# AGENTS.md — 本仓库工作约定

> 供在此仓库工作的编程智能体（Codex / ZCode / DeepSeek harness / Claude Code / Cursor 等）阅读。人写的完整维护手册见 [MAINTENANCE.md](MAINTENANCE.md)。

## 这是什么仓库
「Codex Task Mastery」：一套任务总控技能包（`skills/`，10 个技能）+ 研究底稿。技能遵循 [Agent Skills 官方规范](https://agentskills.io/specification)。福建代账业务提示词在独立私有仓 `fj-daizhang-prompts`。

## 布局
- `skills/` — 技能源码（**唯一可编辑副本**；不要直接改 `~/.codex/skills/` 里的安装副本）
- `_research/` — 外部研究底稿与对标报告（只读参考；无许可证来源仅存摘要+链接）
- `install-skills.ps1` / `lint-skills.py` — 安装同步与规范检查工具
- `.omx/`、`output/` — 运行时状态与产物，不入库

## 协作流程（本项目最高约定）
- 用户直接阐述需求 → 直接工作，产出「可直接粘贴运行」的结构化 AI 提示词（【目标】【背景】【范围】【要求】【完成标准】【输出格式】【验证】）。
- 需求不明时以问答澄清：一次只问一个问题，附上自己的猜测与置信度；**不明确前不动手**。
- 禁止在需求不明时按假设交付或擅自扩大范围。
- 简单明确的小需求直接给结果，不套流程。

## 验证命令（改动后必须跑）
```bash
python lint-skills.py                                                    # 技能规范 + 登记一致性检查
python lint-skills.py --self-test                                        # 校验器自测试（改 lint-skills.py 后必跑）
powershell -ExecutionPolicy Bypass -File install-skills.ps1 -Mode check  # 源与安装端一致
bash install-skills.sh --mode check                                      # macOS/Linux 等价校验（--dest 可指向其它 harness）
```

## 约定
- 改 `skills/` 后：lint → commit → `install-skills.ps1`（安装）→ 新会话生效。
- 新增技能必须同时登记三处：README 技能表、`codex-mastery` 路由表（流程技能）、CHANGELOG。
- 遵循本仓库技能包自身的纪律：证据收口（没跑的验证不说"完成"）、范围纪律（不顺手重构）、简单任务不过度流程化。
- 所有变更记录进 CHANGELOG.md；仓库版本用 semver。
- 第三方内容红线：不新增第三方图片 / 音频 / 无许可证逐字拷贝；引用外部给链接即可，确需引入内容片段须许可证明确并登记 NOTICE.md。
