# 研究笔记：michaelshimeles/skills（摘要 + 链接）

> 说明：本文件原为源仓库 README 的逐字拷贝；因源仓库未声明许可证（All rights reserved），已于 2026-10-31（v1.5.0）降级为「摘要 + 链接」，原文拷贝移出公开仓库。

- 来源：https://github.com/michaelshimeles/skills（研究时快照）
- 性质：Claude Code 技能集，经 `npx skills add` 安装，技能按 description 自动触发。

## 核心机制（研究观察）
1. **四拍工作流**：其 AGENTS.md 把各技能串成「隔离（独立 worktree 起新任务）→ 构建（分层架构约定）→ 证明（测试时录证据）→ 交付（前后对比截图 + 评审循环）」的完整链路。
2. **证据驱动测试**：UI 测试时由代理边操作边录像，注解带时间戳烧录进证据视频，连同结果摘要贴到 PR 与 Issue——用可核验的产物替代口头声称；无头环境降级为脚本化截图。
3. **任务隔离**：每个新任务从 origin/main 切独立 git worktree，支持多代理并行互不冲突，合并后清理。
4. **Vendor + 本地化改造**：第三方技能收入时附带其许可证文件（license included in the folder），并按本地触发习惯改写 frontmatter 触发描述。
5. **其他技能形态**：actions / service 两层架构约定、去除 AI 腔的写作技能、PR 评审循环至满分等。

## 本仓库借鉴的对应关系
- 「隔离 → 构建 → 证明 → 交付」四拍节奏 → 本仓库 `plan-slices` → `verify-claim` 的交付链与「每片处于干净可回滚状态」。
- 「交付必须带证据产物」的形态（其视频证据 vs 本仓库的文字证据循环）→ `verify-claim` 的证据化汇报。
- vendor 附许可证的收编方式 → 本仓库 NOTICE.md 的归属登记做法。
