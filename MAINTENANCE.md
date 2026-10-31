# MAINTENANCE.md — 维护手册

> 面向维护本仓库的人与编程智能体。三份清单 + 工具 + 触发自测。改任何东西之前，先找到对应清单。

## 1. 版本规则
- **仓库版本**（CHANGELOG.md 顶部）：semver——`主.次.修`；技能/工具/文档的实质变更都至少 bump 次版本。
- **提示词版本**：福建代账执行提示词自带 `vX.Y` 头部修订记录，与仓库版本相互独立。
- 提交粒度：一次提交对应一个可说明的变更主题；禁止混入无关改动。

## 2. 清单 A：改一个现有技能
1. 只改 `skills/<技能>/` 下文件；不动安装副本。
2. 跑 `python lint-skills.py` → 通过。
3. 若改了触发语义（description），跑第 5 节该技能的触发自测。
4. 若涉及技能增删或路由变化：同步 README 技能表 + `codex-mastery` 路由表。
5. CHANGELOG 记一行 → git commit。
6. 安装（Windows：`install-skills.ps1`；macOS/Linux：`./install-skills.sh`）→ 重启智能体并新开会话生效。

## 3. 清单 B：新增一个技能
1. 目录名 = name = 小写字母数字+单连字符（1-64 位）；建 `skills/<name>/SKILL.md`。
2. frontmatter：`name` + `description`（≤1024 字符，写清"做什么 + 何时用 + 何时不用"，中英双语触发词）。
3. 正文 <500 行；长内容放 `references/`，可复算逻辑放 `scripts/`（自包含、明确依赖）；每文件都要被 SKILL.md 引用。
4. `python lint-skills.py` → 通过；触发自测补 2-3 条用例到第 5 节。
5. **三处登记**：README 技能表、`codex-mastery` 路由表（流程技能才登记；领域技能在路由表注记区说明）、CHANGELOG。
6. 走清单 A 第 5-6 步收尾。

## 4. 清单 C：维护福建代账提示词（防漂移）
- 唯一事实源：`福建代账智能体-执行提示词.md`。改它 → bump 头部 vX.Y 并写修订记录。
- `精简版`：按新版本手工同步要点（任务定位/意图/方法/适配/边界/红线/政策/质量/验收/顺序十要素齐全）。
- `分段粘贴/`：按新版重新切 8 段；每段首行 `<!-- 从属：… v1.X（日期）｜ 第 N/8 段 -->`；切完必须校验拼接还原：
  ```bash
  cat 分段粘贴/第*段-共8段.md | grep -v '^<!--' | diff - 福建代账智能体-执行提示词.md && echo 一致
  ```
- `启动指令` 若引用路径/结构变化需同步。
- CHANGELOG 记录。

## 5. 触发自测用例（轻量评估）
在**新会话**中发送左列话术，预期加载右列技能（加载错误的即为回归）：

| 话术 | 预期触发 |
|---|---|
| 「开始工作：帮我把这堆发票照片整理成月度账」 | start-work |
| 「帮我做个后台」 | task-brief（缺 who/why/成功标准） |
| 「帮我优化这个提示词」 | prompt-forge（顾问模式，不执行） |
| 「太长了，给我 25% 短版」 | context-budget |
| 「这个任务要改 12 个文件，先拆步」 | plan-slices |
| 「写个通用的 PDF 解析工具」 | repo-first |
| 「你确定修好了？给证据」 | verify-claim |
| 「怎么让 Codex 少返工、省 token」 | codex-mastery（路由） |
| 「还原双色球视频里的选号方法」 | lottery-number-analysis |
| 「大乐透怎么选号，依据是什么」 | lotto-number-pick |
| 反例：「把这个错别字改了」 | **不**加载任何流程技能（简单任务直做） |

## 6. 工具箱
| 工具 | 用途 | 命令 |
|---|---|---|
| `lint-skills.py` | 技能规范 + 登记一致性检查（frontmatter/引用/行数/四处登记互校；错误退出码 1，CI 已接入）；`--self-test` 为校验器自测试 | `python lint-skills.py` |
| `install-skills.ps1` | 安装/同步技能（幂等，只重建有差异的技能） | `powershell -ExecutionPolicy Bypass -File install-skills.ps1` |
| `install-skills.sh` | bash 跨平台版安装/同步（行为同 ps1；`--dest` 指定多 harness 目标，`--mode check` 检漂移） | `./install-skills.sh` |
| 同上 check 模式 | 只检测源与安装端漂移，不改动 | 同上 + ` -Mode check` |

## 7. 已决事项与有意取舍
- LICENSE：已采用 MIT（2026-10-30 收口，见 CHANGELOG v1.3.0）。如需更换版权署名，改 LICENSE 版权行即可。
- 第三方内容收敛到最小集（2026-10-31，v1.5.0）：视频帧证据图移出仓库；无许可证来源降级为摘要+链接；MIT 来源逐字拷贝保留并附完整许可文本（见 NOTICE.md）。**后续不得新增第三方图片或无许可证逐字拷贝**（红线见 CONTRIBUTING.md）。
- 按技能粒度的版本元数据有意未采用（CHANGELOG 已覆盖，避免双重维护）。
