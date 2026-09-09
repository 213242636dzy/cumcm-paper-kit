# CUMCM Paper Kit

面向全国大学生数学建模竞赛论文交付的 Codex skill。它以仓库内的 Word 与 LaTeX 模板为版式基准，把赛题、数据、代码、真实运行结果、图表、参考文献、附录和 AI 使用记录连成可核验的论文闭环。

## 适合做什么

- 按 Word 或 LaTeX 模板写整篇论文或指定章节；
- 从真实数据与计算结果生成论文图、流程图和表格；
- 检查摘要、模型、数值、图表、引用、附录和支撑材料的一致性；
- 生成并核对 2026 年要求的 AI 工具使用声明与详情材料；
- 审计页序、目录、匿名性、占位符、文件大小和提交包。

它不替代建模本身，也不会把候选方法、未运行代码或示例数字写成已完成结果。

## 仓库结构

```text
skills/cumcm-paper-kit/
  SKILL.md
  agents/openai.yaml
  assets/
    templates/
    ledgers/
  references/
  scripts/
```

模板资产来自仓库所有者提供的本地材料，适用权利边界见 `THIRD_PARTY_NOTICES.md`，因此仓库默认应保持私有。公开发布前应确认模板、字体和示例文件的再分发授权；竞赛期间不得向 GitHub 上传或讨论当届赛题、解答、队伍草稿、数据或代码。

Word 路线内含两个不同用途的文件：`CUMCM-2026-论文空白模板.docx` 是可直接写作的干净骨架；`2026年数学建模竞赛论文模板.docx` 是原始彩色说明手册，只用于核对版式与操作说明。LaTeX 初始化器会保留原压缩包，并在工作副本中自动修正 2026 规则下不应出现的目录与页码重置。

## 安装

使用 Codex 的 skill 安装器从仓库安装 `skills/cumcm-paper-kit`，或把这个目录链接到 `~/.codex/skills/cumcm-paper-kit`。重新加载 Codex 后，可用 `$cumcm-paper-kit` 显式调用，也可由相关任务自动触发。

## 本地验证

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/cumcm-paper-kit
python skills/cumcm-paper-kit/scripts/audit_submission.py --help
python skills/cumcm-paper-kit/scripts/cumcm_plot_style.py --demo /tmp/cumcm-figure-demo.svg
```

## 参考思路

结构与工作流设计参考了 GitHub 上公开数模 skills 的可取模式，包括轻量入口与按需 references、问题到证据的可追溯链、确定性审计脚本、基线/主模型/验证的分层。本仓库聚焦模板驱动的论文与提交交付，不复制第三方 skill 内容或历史论文原文。
