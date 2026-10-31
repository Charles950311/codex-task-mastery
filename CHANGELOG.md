# CHANGELOG

记录本仓库（Codex Task Mastery 技能包 + 福建代账智能体提示词）的变更。
福建代账提示词自身的版本见各文件头部（当前 v1.2）；本文件的版本号针对仓库整体与 `skills/` 技能包。

## [1.5.0] - 2026-10-31

### 公开发布安全加固：第三方内容收敛到最小集
- **移除两张第三方视频帧证据图**：`skills/lottery-number-analysis/references/evidence/video-frames.jpg` 与 `skills/lotto-number-pick/references/evidence/video-frames.jpg`。图片不具备文字那样的「研究引用」惯例空间，版权暴露风险高；方法溯源证据由各技能 `references/source-evidence.md` 的逐节文字时间轴完整承载，原始帧与视频仍在研究工作区（`双色球` / `大乐透` 目录，未入库）。同步更新 7 处引用（两个 SKILL.md、两个 source-evidence.md、ssq-case-study.md、method-and-math.md、NOTICE.md）；`.gitignore` 增加 `skills/*/references/evidence/` 防回填。
- **三个无许可证仓库的原文拷贝降级为「摘要 + 链接」**（同文件名，逐字拷贝移出公开仓库）：`_research/Mai-xiyu__Codex-Prompt.md`（注：源 README 自述 MIT 但无独立 LICENSE 文件，按无许可证从保守处理）、`_research/composio-community__awesome-codex-skills.md`、`_research/michaelshimeles__skills.md`。研究结论（核心机制观察、借鉴对应关系）完整保留。MIT 来源（ECC / addyosmani / FerroxLabs）的逐字拷贝按 MIT 条款保留，并在 NOTICE.md 补上完整 MIT 许可证文本。
- **新增 `CONTRIBUTING.md`**：外部贡献范围（技能 / 工具 / 文档）、必做验证命令、新增技能最小流程、提交约定、第三方内容红线。
- **红线入约**：AGENTS.md 约定区与 MAINTENANCE.md 已决事项各加一条「不新增第三方图片 / 无许可证逐字拷贝」。
- README：版本号、许可证章节表述、维护入口（CONTRIBUTING）、目录结构同步。
- 背景：公开发布前把版权暴露点收敛——文字有「引用」惯例空间且已全部走摘要+归属，图片与无许可证原文是最薄弱的两处。

## [1.4.0] - 2026-10-30

### 公开发布前：第三方内容归属
- 新增 `NOTICE.md`：登记 `_research/` 中逐字拷贝的第三方内容——MIT 来源（ECC / addyosmani / FerroxLabs，附版权行）与三个未声明许可证的仓库（Mai-xiyu / composio-community / michaelshimeles，标注仅作研究引用）；声明本仓库 MIT 仅覆盖原创内容；注明两张视频帧证据图的来源。
- README：许可证章节补 `NOTICE.md` 入口；目录结构补 `NOTICE.md`；版本升至 v1.4.0。
- 背景：首次公开推送到 GitHub 前的发布前检查发现 `_research/` 含第三方原文拷贝，按最稳妥方式补充归属而非删除内容。

## [1.3.0] - 2026-10-30

### 待决收口：仓库许可证
- 新增 `LICENSE`：采用 **MIT** 许可证（版权行 `Copyright (c) 2026 Administrator`，可随时改为真实姓名/团队）。关闭 v1.2.0 标注的唯一待决事项「仓库 LICENSE」。
- README：头部标注许可证，新增「许可证」章节（第三方项目归各自作者所有；技能与提示词为本仓库原创设计/改写）；目录结构补 `LICENSE`。
- MAINTENANCE.md：第 7 节「已知待决事项」改为「已决事项与有意取舍」——LICENSE 转为已决，其余条目均为有意取舍而非待决。

## [1.2.0] - 2026-10-24

### 商业对标与专业化（对标 Agent Skills 官方规范 / Codex / Cursor / AGENTS.md 标准）
- 新增 `lint-skills.py`：按官方 spec 校验技能（name 命名规则 / description ≤1024 / SKILL.md <500 行 / 引用文件存在 / 孤儿文件告警；错误退出码 1 可接 CI）。已双向测试：本仓库 10/10 通过；坏技能样本 3 类错误全捕获。
- 新增 `AGENTS.md`：跨编程智能体（Codex / ZCode / DeepSeek harness 等）通用的仓库约定入口——布局、验证命令、改动纪律。
- 新增 `MAINTENANCE.md`：维护手册——版本规则、改技能/新增技能/提示词派生三份同步清单、11 条触发自测用例（轻量评估）、工具箱。
- README 专业化升级：仓库全景表、快速上手、维护入口、全仓库目录结构；技能合规声明（Agent Skills 官方规范）。
- 新增 `_research/商业对标-2026-10.md`：14 项逐项差距判定（含有意不采用项的理由与来源）。
- 审计证据：两个彩票 Python 脚本实测跑通且输出与文档数值一致；10 个技能 frontmatter / 引用完整性 / 行数全部合规。
- 待决：仓库 LICENSE（法律决定，未代做；已于 1.3.0 收口为 MIT）。

## [1.1.0] - 2026-10-24

### 项目开展提示词（提示词层升级，业务内容不变）
- **福建代账智能体-执行提示词 v1.2**：新增【任务定位】【意图】【跨 Harness 适配约定】【工作方法】四节；【自动化与合规边界】前置（原【自动化边界】上移合并，避免重复）；全文「Codex」改称「执行智能体」，GitHub 检索 / 视觉识别 / 技能包安装给出降级链；AC-1 与政策基线日期等环境绑定表述通用化。数据契约、要求 A-F、验收 AC-0~8、里程碑 M0-M6 与 v1.1 完全一致（未做内容升级）。
- **福建代账智能体-启动指令 v1.2**：新增「先复述理解 + 假设与置信度」「每阶段证据收口」要求，并声明适用于任意编程智能体。
- **福建代账智能体-精简版 v1.2**：同步新结构（任务定位 / 意图 / 方法 / 适配降级）。
- **分段粘贴/**：按 v1.2 重新切分 8 段，每段首行加 HTML 注释（从属版本 + 段号）；已验证 8 段按序拼接与全文逐字节一致。
- **新增 项目开展提示词-通用骨架.md**：跨编程智能体（Codex / DeepSeek harness / ZCode 等）开工提示词的通用写法——意图先行、方法内联、降级成文、措辞合规化（明确定位 + 红线成文，不软化红线）、完成标准可验证、单一事实源。

## [1.0.0] - 2026-10-24

### 基建
- 纳入 git 版本管理：首提交为全部存量内容的基线快照（2b8424a），此后每次改动可追溯、可回滚。
- 新增 `install-skills.ps1`：`skills/` → `~/.codex/skills` 的安装与同步脚本。
  - `-Mode check`：只检测两端漂移（未安装 / 内容差异 / 目标端多余文件），漂移时退出码 1，可用于定期自检；
  - 默认 install 模式：只重建有差异的技能目录（能清掉源端已删除的文件），幂等，绝不触碰 `.system` 等非本包目录；
  - 已实测：空目标安装 10 技能、幂等重装 0 更新、篡改 + 多余文件场景下检测并修复、修复后 check 干净。
- 新增 `.gitignore`：排除 `.omx/` 运行时状态、`output/` 月度归档产物、Python 缓存等。

### 文档
- README「安装」章节改为脚本优先，保留手动复制作为降级方式，并新增仓库版本标注。

### 技能（本版为基线快照，无内容改动）
- 8 个流程技能：codex-mastery / start-work / task-brief / prompt-forge / context-budget / plan-slices / repo-first / verify-claim。
- 2 个领域技能：lottery-number-analysis / lotto-number-pick。
