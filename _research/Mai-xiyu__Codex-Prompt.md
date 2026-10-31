# 研究笔记：Mai-xiyu/Codex-Prompt（摘要 + 链接）

> 说明：本文件原为源仓库 README 的逐字拷贝；因源仓库无独立 LICENSE 文件（All rights reserved 从保守处理），已于 2026-10-31（v1.5.0）降级为「摘要 + 链接」，原文拷贝移出公开仓库。
> 源 README 自述「MIT License」，但截至研究快照时仓库未附独立 LICENSE 文件，故仍按无许可证处理。

- 来源：https://github.com/Mai-xiyu/Codex-Prompt
- 配套仓库：[Mai-xiyu/wide-lens-engineering](https://github.com/Mai-xiyu/wide-lens-engineering)（执行 / 编排层 Skill，源仓库建议与其搭配使用）

## 这是什么
一个面向工程、技术分析与高准确性回答场景的通用系统提示词：让模型把正确性置于迎合之上，按「结论 → 分析 → 建议」的工程风格输出，并对安全研究场景给出攻击 / 防御双视角约定。

## 核心机制（研究观察）
1. **事实核验优先**：外部事实、时间敏感信息先联网核验；核验失败时明确标记「未核验」，只继续本地证据能支持的工作；不把搜索片段或推测说成已验证事实。
2. **信息类型分级**：回答中显式区分事实 / 推测 / 最佳实践 / 社区共识 / 官方文档结论。
3. **低信息密度禁令**：禁止机械式礼貌、营销语言、AI 套话、情绪化共鸣与重复总结。
4. **工程化回答约定**：代码答案要求可运行 + 复杂度标注 + 适用场景与局限 + 异常 / 安全 / 可维护性考量；系统设计问题必须给 trade-off 而非「标准答案」。
5. **安全研究双视角与非武器化**：漏洞分析覆盖根因 / 前置条件 / Exploitability / CWE / CVSS，PoC 优先无害化最小化，同时给修复、检测与上报建议。
6. **自主执行与完成边界**：在授权范围内自主推进、合理默认；但不得用计划、部分实现或未运行的测试宣称完成，受阻时不得把受阻报告标记为成功。
7. **Prompt 与 Skill 分层**：Codex-Prompt 只做行为 / 推理层；任务拆解、动态 DAG、单一写入者、失败恢复由 wide-lens-engineering 承担，两者独立可用、可组合。

## 本仓库借鉴的对应关系
- 「不编造、未验证不称完成」→ `verify-claim` / `task-brief` / `start-work` 的红线。
- 「显式不确定性、区分事实与推测」→ `codex-mastery` / `task-brief` 的假设暴露与置信度机制。
- 「理性克制、该反对就反对」→ `codex-mastery` 的反对义务条款。
- wide-lens-engineering 的「弹性任务 DAG、单一 canonical writer、失败恢复」→ `plan-slices` 的单一写入者与失败即停。
