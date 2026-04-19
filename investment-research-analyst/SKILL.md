---
name: investment-research-analyst
description: 投研经理工作流；当用户需要行业研究、宏观分析、研报获取、财务分析或撰写投资报告时使用
dependency:
  python:
    - requests>=2.31.0
    - beautifulsoup4>=4.12.0
    - lxml>=4.9.0
---

# 投研经理工作流

## 任务目标
- 本 Skill 用于：执行从宏观经济分析到行业深度研究、研报获取、财务分析和投资逻辑梳理的完整投研工作流
- 能力包含：宏观周期研判、行业分析、研报爬取、财务指标分析、估值建模、投资报告撰写
- 触发条件：用户要求进行投资研究、分析行业趋势、评估公司价值、获取行业研报或撰写投研报告

## 前置准备
- 依赖说明：scripts 脚本所需的依赖包及版本
  ```
  requests>=2.31.0
  beautifulsoup4>=4.12.0
  lxml>=4.9.0
  ```

## 操作步骤
- 标准流程:
  1. **确定研究范围与目标**
     - 智能体与用户确认研究目标（宏观/行业/公司层面）
     - 明确研究深度和输出形式

  2. **宏观环境分析**（如适用）
     - 智能体基于 [references/macro-framework.md](references/macro-framework.md) 的分析框架，研判当前经济周期
     - 分析货币政策、财政政策、监管环境对目标领域的影响

  3. **行业研究**（核心环节）
     - 智能体基于 [references/industry-framework.md](references/industry-framework.md) 进行行业深度分析
     - 调用 `scripts/fetch_reports.py` 获取目标行业的最新研报，命令格式：
       ```bash
       python /workspace/projects/investment-research-analyst/scripts/fetch_reports.py --industry <行业名称> --days <获取近N天的研报>
       ```
     - 基于研报数据，智能体分析行业空间、竞争格局、产业链结构、发展趋势

  4. **财务分析**（如涉及公司层面）
     - 智能体基于 [references/financial-metrics.md](references/financial-metrics.md) 识别关键财务指标
     - 解析财报数据，评估盈利能力、成长性、财务风险
     - 进行估值建模（DCF、PE、PB 等多维度）

  5. **投资逻辑梳理与报告撰写**
     - 智能体基于 [assets/report-template.md](assets/report-template.md) 模板撰写投研报告
     - 报告包含：投资逻辑、核心观点、风险提示、操作建议

- 可选分支:
  - 当仅需研报数据：执行步骤3的研报获取环节，输出结构化研报摘要
  - 当仅需宏观分析：执行步骤2，输出宏观环境研判报告
  - 当仅需财务分析：执行步骤4，输出财务指标分析报告

## 资源索引
- 必要脚本:见 [scripts/fetch_reports.py](scripts/fetch_reports.py)(用途与参数:爬取东方财富等主流研报平台的行业研报，支持 --industry 指定行业、--days 指定天数)
- 领域参考:
  - [references/macro-framework.md](references/macro-framework.md)(何时读取:进行宏观分析时)
  - [references/industry-framework.md](references/industry-framework.md)(何时读取:进行行业研究时)
  - [references/financial-metrics.md](references/financial-metrics.md)(何时读取:进行财务分析时)
- 输出资产:见 [assets/report-template.md](assets/report-template.md)(直接用于生成/修饰输出)

## 注意事项
- 研报爬取脚本可能受网站反爬限制，建议分批次获取，避免短时间内大量请求
- 财务分析需结合行业特性，不同行业关注的指标权重不同（如科技行业看重研发投入，消费行业看重品牌价值）
- 投资逻辑需基于数据和事实，避免主观臆断，充分披露风险因素
- 充分利用智能体的分析与生成能力，仅在涉及数据爬取等技术性任务时调用脚本

## 使用示例

### 示例1：新能源汽车行业深度研究
- 功能说明：完成从宏观到行业的完整投研分析
- 执行方式：智能体主导分析流程，脚本获取研报数据
- 关键要点：
  - 基于宏观框架分析新能源政策支持力度
  - 调用脚本获取新能源汽车行业最新研报
  - 分析产业链上下游竞争格局
  - 基于模板输出深度研究报告
- 命令示例：
  ```bash
  python /workspace/projects/investment-research-analyst/scripts/fetch_reports.py --industry "新能源汽车" --days 30
  ```

### 示例2：半导体行业研报快速获取
- 功能说明：获取指定行业的最新研报并生成摘要
- 执行方式：脚本爬取 + 智能体摘要
- 关键参数：--industry 指定行业名称，--days 控制时间范围
- 命令示例：
  ```bash
  python /workspace/projects/investment-research-analyst/scripts/fetch_reports.py --industry "半导体" --days 7
  ```

### 示例3：消费行业公司财务分析
- 功能说明：分析目标公司的财务健康状况与投资价值
- 执行方式：智能体基于财务指标框架进行分析
- 关键要点：重点关注 ROE、毛利率、营收增速、现金流等核心指标
