# CHANGELOG

记录本仓库（Codex Task Mastery 技能包 + 福建代账智能体提示词）的变更。
福建代账提示词自身的版本见各文件头部（当前 v1.1）；本文件的版本号针对仓库整体与 `skills/` 技能包。

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
