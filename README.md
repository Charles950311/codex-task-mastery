# Codex Task Mastery — 技能包

一套面向 Codex 的“任务总控”技能包：让 Codex **更理解任务目的、更高效地执行、更省时间与 token、并用证据把目标真正达成**。

> 仓库版本：**v1.6.0**（2026-10-31，变更记录见 [CHANGELOG.md](CHANGELOG.md)）｜ 本仓库已纳入 git 版本管理 ｜ 许可证：[MIT](LICENSE)
> 技能遵循 [Agent Skills 官方规范](https://agentskills.io/specification)，兼容 Codex / Claude Code 等生态

## 仓库全景

| 资产 | 位置 | 说明 |
|---|---|---|
| 任务总控技能包 | `skills/` | 8 个流程技能 + 2 个领域技能，安装到技能目录后自动触发 |
| 项目开展提示词 | `福建代账智能体-*.md`、`分段粘贴/` | 福建代账智能体：执行提示词 v1.2（唯一事实源）+ 精简版 + 启动指令 + 8 段粘贴版 |
| 通用方法论 | `项目开展提示词-通用骨架.md` | 跨编程智能体的开工提示词写法（意图先行/方法内联/降级成文） |
| 工具链 | `install-skills.ps1`、`lint-skills.py`、GitHub Actions | 安装同步（漂移检测）+ 规范与登记一致性校验（校验器自带自测试，已接 CI） |
| 研究底稿 | `_research/` | 技能来源研究 + 商业项目对标报告 |
| 维护文档 | `MAINTENANCE.md`、`AGENTS.md` | 维护手册（同步清单/触发自测）；AGENTS.md 供编程智能体读取仓库约定 |

## 快速上手
```powershell
# 1. 安装技能（./skills → ~/.codex/skills，幂等）
powershell -ExecutionPolicy Bypass -File .\install-skills.ps1

# 2. 校验（可选）：技能规范 + 源与安装端一致性
python lint-skills.py
powershell -ExecutionPolicy Bypass -File .\install-skills.ps1 -Mode check

# 3. 重启 Codex 并新开会话，技能元数据即被加载
```

日常使用只需两步：描述任务（自动按 description 匹配触发），或点名技能（如“用 `task-brief` 先对齐需求”）。要跑福建代账项目，直接把 `福建代账智能体-启动指令.md` 的内容发给任意编程智能体。

## 它解决什么问题
| 常见失败 | 本技能包的对应技能 |
|---|---|
| 收到「开始工作」却不知从何下手，提示词不够可执行 | `start-work` |
| 没搞清“到底要什么”就动手，返工 | `task-brief` |
| 提示词含糊、没有完成标准、无法验收 | `prompt-forge` |
| 上下文越滚越大，变慢、变贵、注意力涣散 | `context-budget` |
| 一次改一大坨，出错难定位、难回滚 | `plan-slices` |
| 重复造轮子、引入无谓依赖 | `repo-first` |
| 自信地说“做完了”，其实没验证 | `verify-claim` |
| 不知道该用哪个技能 | `codex-mastery`（路由） |

## 包含的技能
| 技能 | 作用 | 触发场景 |
|---|---|---|
| `codex-mastery` | 元技能 / 总控路由，串起整套流程 | 目标不清、跨多步骤、要省 token / 提质量 |
| `start-work` | 工作流入口：诉求 → 可执行提示词 + 路由 | 用户说「开始工作」+ 任务诉求 |
| `task-brief` | 把模糊请求转成可验收简报 | “帮我做 X”却没说清谁 / 为什么 / 成功标准 |
| `prompt-forge` | 生成 / 优化可直接运行的 Codex 提示词 | “写个提示词”“优化 prompt”“怎么写指令” |
| `context-budget` | 上下文与 token 预算管理 | 会话变长、要省 token / 时间、控制回复长度 |
| `plan-slices` | 切片 + 增量执行 + 单一写入者 | 跨多文件、需可回滚的增量交付 |
| `repo-first` | 先搜后写，复用优先 | 要写新功能 / 工具 / 依赖 |
| `verify-claim` | 交付前证据化验证 + 怀疑循环 | 要声称完成、要合并 / 发布、高风险决策 |
| `lottery-number-analysis` | 双色球 / 大乐透选号方法的参数化数学复现（科普） | 要还原 / 讲解 / 复现彩票选号方法、算组合数 / 中奖概率 / 期望值、比较两彩种 |
| `lotto-number-pick` | 大乐透选号方法的数学复现（专例·科普） | 要还原 / 讲解 / 复现大乐透选号方法与数学依据 |

## 使用方式
- **自动触发**：描述任务时，Codex 会按 `description` 匹配并加载相应技能。
- **显式调用**：直接点名，例如“用 `task-brief` 先把需求问清楚”“用 `prompt-forge` 优化这个提示词”。
- **「开始工作」工作流**：说「开始工作」+ 一段任务诉求 → `start-work` 先对齐目标与验收，再改写成可直接执行的提示词，并给出后续技能链。
- **推荐主流程**：`codex-mastery`（路由）-> `start-work`（诉求 → 可执行提示词）-> `plan-slices`（拆步执行）-> `verify-claim`（证据收口）；目标不清先 `task-brief`，全程 `context-budget` 控开销，写新东西先 `repo-first`。

简单、明确、单步、低风险的任务**直接做**，不要套流程——这本身就是 `context-budget` 的要求。

## 安装与同步
技能源位于本仓库 `skills/`。推荐用仓库自带的同步脚本（自动检测漂移，只覆盖有差异的技能）：

```powershell
# 安装 / 更新：./skills → ~/.codex/skills（幂等，可重复运行）
powershell -ExecutionPolicy Bypass -File .\install-skills.ps1

# 只检测源与安装端是否一致，不改动任何文件；有漂移时退出码 1，可用于定期自检
powershell -ExecutionPolicy Bypass -File .\install-skills.ps1 -Mode check
```

脚本行为：install 按整目录重建有差异的技能（能清掉源端已删除的文件），只处理本包的技能目录，不触碰 `~/.codex/skills/` 下其它内容（如 `.system`）。

也可手动复制（缺点：不清理源端已删除的文件，也无法发现漂移）：

```powershell
Copy-Item -Recurse -Force ".\skills\*" "$env:USERPROFILE\.codex\skills\"
```

然后**重启 Codex 并新开会话**，技能元数据才会被加载。

## 维护
- 改技能 / 新增技能 / 改提示词：按 [MAINTENANCE.md](MAINTENANCE.md) 的三份同步清单执行；改动后跑 `python lint-skills.py`。
- 外部贡献：见 [CONTRIBUTING.md](CONTRIBUTING.md)。
- 编程智能体在本仓库工作时的约定见 [AGENTS.md](AGENTS.md)。
- 触发自测用例（验证技能仍被正确触发）见 MAINTENANCE.md 第 5 节。

## 许可证
本仓库原创内容采用 [MIT](LICENSE) 许可证。`_research/` 中 MIT 来源的原文拷贝按原许可证附归属保留；无许可证来源仅存摘要与链接，第三方视频帧证据图已移除——归属与状态详见 [NOTICE.md](NOTICE.md)；技能正文与提示词均为面向本项目的重新设计与改写，非原文照搬（见「研究与来源」说明）。

## 设计原则（来自对头部开源技能的研究）
1. **目的优先于动作**：先锁定“可观察的结果”，再谈怎么实现。
2. **一切以可验证为准**：没有证据不说“完成”。
3. **渐进披露**：`SKILL.md` 只放必要内容，长清单进 `references/`，按需加载。
4. **描述即触发器**：`description` 写清“何时用 / 何时不用”，中英双语关键词以提升匹配率。
5. **不制造流程负担**：简单任务直接做，只在真正有价值时加载技能。
6. **对抗 AI 的默认倾向**：迎合、猜、过度设计、顺手改范围、假装完成——逐条设红线。

## 研究与来源
本技能包是对 GitHub 上高星 / 高热度 Codex、Claude 技能与系统提示词做交叉研究后，抽取其核心机制并针对 Codex 场景优化合并而成。主要参考（按研究时的星标量级）：

| 仓库 | 星标量级 | 借鉴的核心机制 |
|---|---|---|
| `affaan-m/ECC` | ~27 万 | 技能 / 规则 / 钩子分层、`prompt-optimizer`、`token-budget-advisor`、`context-budget`、`verification-loop`、`search-first`、`iterative-retrieval`、验收简报 |
| `addyosmani/agent-skills` | ~10 万 | `using-agent-skills` 路由、`context-engineering`、`interview-me`、`doubt-driven-development`、`planning-and-task-breakdown` |
| `ComposioHQ/awesome-claude-skills` | ~7.6 万 | 技能目录组织与安装约定 |
| `VoltAgent/awesome-agent-skills` | ~3.5 万 | 跨工具技能规范 |
| `composio-community/awesome-codex-skills` | ~1.7 万 | Codex 技能结构与前端触发约定 |
| `cobusgreyling/loop-engineering` | ~1.1 万 | 循环 / 编排工程模式 |
| `michaelshimeles/skills` | 上千 | 隔离 -> 构建 -> 证明 -> 交付的四拍工作流 |
| `FerroxLabs/agents-md` | 上千 | “每个改动都可追溯到请求”“先写验证再报告” |
| `Mai-xiyu/Codex-Prompt` | 数百 | 理性克制、显式不确定性、可运行方案 |
| `Mai-xiyu/wide-lens-engineering` | — | 弹性任务 DAG、单一 canonical writer、失败卡片 |

2026-10 起另按官方规范与商业实践做了一轮对标（Agent Skills spec / Codex / Cursor / AGENTS.md 标准），差距判定与落地动作见 [_research/商业对标-2026-10.md](_research/商业对标-2026-10.md)。

> 说明：星标量为研究时快照，仅用于体现“热门程度”与选材依据；技能正文为面向本项目的重新设计与改写，非原文照搬。

## 目录结构
```
.
├─ LICENSE（MIT）/ NOTICE.md / CONTRIBUTING.md / README.md / CHANGELOG.md / AGENTS.md / MAINTENANCE.md
├─ install-skills.ps1            安装与同步（install / check 双模式）
├─ lint-skills.py                技能规范 + 登记一致性校验（按 Agent Skills 官方 spec）
├─ .github/workflows/ci.yml      CI：校验器自测试 + 规范/登记检查 + 拼接校验 + 安装同步自检
├─ skills/                       技能源码（安装源）
│  ├─ start-work/                ├─ references/workflow-and-output.md
│  ├─ codex-mastery/             ├─ task-brief/（references/acceptance-brief.md）
│  ├─ prompt-forge/              ├─ references/prompt-patterns.md
│  ├─ context-budget/            ├─ references/token-and-compaction.md
│  ├─ plan-slices/ ├─ repo-first/ ├─ verify-claim/
│  ├─ lottery-number-analysis/   ├─ references/ + scripts/lottery_math.py
│  └─ lotto-number-pick/         └─ references/ + scripts/structural_pick.py
├─ 福建代账智能体-执行提示词.md   v1.2（唯一事实源）
├─ 福建代账智能体-精简版.md / 启动指令.md
├─ 分段粘贴/                     执行提示词 8 段粘贴版（从属 v1.2）
├─ 项目开展提示词-通用骨架.md
└─ _research/                    研究底稿（MIT 原文拷贝 + 无许可证来源摘要）+ 商业对标报告
```
