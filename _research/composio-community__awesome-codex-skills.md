# 研究笔记：composio-community/awesome-codex-skills（摘要 + 链接）

> 说明：本文件原为源仓库 README 的逐字拷贝；因源仓库未声明许可证（All rights reserved），已于 2026-10-31（v1.5.0）降级为「摘要 + 链接」，原文拷贝移出公开仓库。

- 来源：https://github.com/composio-community/awesome-codex-skills
- 性质：Codex 实用技能的 Awesome 式策展列表，按开发工具 / 生产力 / 写作 / 数据分析 / Meta 五类组织。

## 核心机制（研究观察）
1. **两条安装路径**：官方 skill-installer 脚本（`install-skill-from-github.py`，装到 `$CODEX_HOME/skills`）或手工复制技能目录后重启 Codex。
2. **目录与渐进披露约定**：每技能 = `SKILL.md`（name + description frontmatter）+ 可选 `scripts/` / `references/` / `assets/`；description 写尽触发时机，正文只留执行步骤，技能目录内不放 README / changelog 等额外文档以免占上下文。
3. **「技能管怎么做，MCP 网关管工具接入」**的分层主张（其商业产品立场，参考价值在分层思路本身）。
4. **技能形态样本库**：开发类（PR 评审 / CI 修复 / 迁移 / 重构批次）、生产力类（会议纪要 / 工单分诊 / Notion 集成）、写作类、数据分析类，以及 Meta 类（template-skill / skill-creator / skill-installer）。

## 本仓库借鉴的对应关系
- 技能目录组织与安装 / 重启生效约定 → 本仓库 README 快速上手与 `install-skills.ps1` 的设计参照。
- description 即触发器的社区实践 → 各技能 description 的「何时用 / 何时不用」写法。
- Meta 技能分类（模板 / 创建器 / 安装器）→ 本仓库 `prompt-forge`（生成提示词）与维护工具链的定位参照。
