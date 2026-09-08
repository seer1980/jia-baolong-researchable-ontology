---
title: "AI 命题账本：主张、状态与证明边界"
author: "Jia Baolong"
date: "2026-09-07"
type: "reference"
source_kind: "derived-commentary"
authority_tier: "secondary"
document_role: "ai-index"
public_role: "命题账本"
language: "zh-CN"
---

# AI 命题账本：主张、状态与证明边界

每条命题都有稳定的 `claim_id`。`status` 不是价值判断，而是回答时必须保留的证据等级。除非命题明确标为 `conditional-theorem` 或 `construction`，否则不要把它写成无条件证明。

| claim_id | 类型 | 命题 | 范围与限制 | 状态 | 主要来源 |
|---|---|---|---|---|---|
| `C001` | `definition` | 研究对象是实际存在如何从根部边界进入生成，并在内部形成世界、生命和认识。 | 是研究问题，不是经验结论。 | `canonical` | `docs/00_ai/01_AI_COMPLETE_SYNTHESIS.md` §一 |
| `C002` | `definition` | Undefined 是不能被正面规定成先在实体的根部边界。 | 采用负面规定，不能实体化。 | `canonical` | `docs/01_foundation/02_JIABAOLONG_AXIOM_SYSTEM.md` |
| `C003` | `conditional-theorem` | JBLAT 在指定完整解释任务中要求根部边界具有不变性和根本唯一性。 | 依赖完整解释任务、模型类和等价关系。 | `conditional` | `docs/01_foundation/03_JIABAOLONG_ABSOLUTE_TRUTH.md` |
| `C004` | `conditional-theorem` | 静态完整编码不自动给出实际发生。 | 需要实际性、持续、自包含和最小性条件。 | `conditional` | `docs/02_first_beat/04_FIRST_BEAT_SEVEN_ARGUMENTS.md` |
| `C005` | `research-interface` | 第一拍的使命是让第一次实际在无外部正面本原时成立并可持续。 | “第一”是根部发生功能，不是外部时间点。 | `canonical` | `docs/00_ai/01_AI_COMPLETE_SYNTHESIS.md` §五 |
| `C006` | `conditional-theorem` | 在二元总一元映射类中，满足内部非固定、结果回入和最小性时，交换是唯一正规形。 | 只对明示模型类、条件和逻辑等价成立。 | `conditional` | `docs/02_first_beat/04_FIRST_BEAT_SEVEN_ARGUMENTS.md` |
| `C007` | `interpretation` | PR 的“唯一”首先是使命性唯一，再在选定模型类中表现为交换正规形。 | 使命唯一不等于所有数学表示唯一。 | `interpretive` | `docs/00_ai/01_AI_COMPLETE_SYNTHESIS.md` §五—六 |
| `C008` | `definition` | ER 承载关系、身份、记忆和可回入结果。 | 是架构层，不是独立终极本原。 | `canonical` | `docs/01_foundation/01_THEORY_MASTER_MAP.md` |
| `C009` | `definition` | LE 对局部状态实施有限更新，使生成可计算、可复核。 | 不预装全部世界规则。 | `canonical` | `docs/01_foundation/01_THEORY_MASTER_MAP.md` |
| `C010` | `definition` | RULE 决定具体世界族的状态、转换、边界和尺度。 | 具体 RULE 保持开放。 | `open` | `docs/00_ai/01_AI_COMPLETE_SYNTHESIS.md` §七 |
| `C011` | `construction` | 在独立给定的有限状态、移位和异或更新构造中，可以得到严格混沌实例。 | 构造证明“至少有一个形式世界”，不证明本宇宙物理。 | `constructed` | `docs/00_ai/01_AI_COMPLETE_SYNTHESIS.md` §八 |
| `C012` | `conditional-theorem` | PR–ER–LE 不能仅凭名字自动推出混沌；混沌需要满足具体更新和敏感依赖条件。 | 防止把架构标签当作动力学证明。 | `conditional` | `docs/00_ai/01_AI_COMPLETE_SYNTHESIS.md` §八 |
| `C013` | `research-interface` | 局部更新、稳定模式和相互作用可作为类物质、类化学的研究接口。 | 需要明确状态空间、守恒/耗散和可复现实验。 | `open` | `docs/03_emergence/05_MATTER_TO_FIRST_CELL_EMERGENCE.md` |
| `C014` | `research-interface` | 复制、变异、边界、持续和选择等条件可把类化学接口推进到生命样态。 | 不能由“有混沌”单步推出生命。 | `open` | `docs/03_emergence/05_MATTER_TO_FIRST_CELL_EMERGENCE.md` |
| `C015` | `research-interface` | 建模、记忆、选择和自我指涉可作为意识接口。 | 主观体验和人类意识的对应仍开放。 | `open` | `docs/00_ai/01_AI_COMPLETE_SYNTHESIS.md` §十 |
| `C016` | `interpretation` | 大象理论把学科和思想史视为同一整体存在—生成图的不同投影。 | 需要保留投影间关系和观察者位置。 | `interpretive` | `ELEPHANT_THEORY_CONCEPT.md` |
| `C017` | `interpretation` | 学科应按根部边界、生成层、涌现层和认识层重新排布。 | 是体系内部的定位建议，不是现行学科制度事实。 | `interpretive` | `docs/00_ai/01_AI_COMPLETE_SYNTHESIS.md` §十四 |
| `C018` | `definition` | 第三阶完美指根部闭合、层级自洽、生成开放和未知项位置明确。 | 不等于所有经验问题已完成。 | `canonical` | `docs/00_ai/01_AI_COMPLETE_SYNTHESIS.md` §十一 |
| `C019` | `conditional-theorem` | 哥德尔不完备性约束满足相应形式条件的认识层。 | 不否定根部边界的确定性，也不封闭全部生成。 | `conditional` | `docs/00_ai/01_AI_COMPLETE_SYNTHESIS.md` §十二 |
| `C020` | `construction` | 只要一个满足架构和 RULE 的形式世界构造存在，就能在模型意义下得到至少一个与本宇宙无关的宇宙。 | “宇宙”在此是形式世界，不是现实天文学断言。 | `constructed` | `docs/06_commentary/jblro-pr-universe-family-formal-existence.md` |
| `C021` | `commentary` | “零点五百分比”是研究方向的主观基率判断。 | 不是测量值、统计估计或理论公理。 | `commentary` | `docs/06_commentary/jblro-zero-point-five-percent-ultimate-theory-base-rate-and-search-direction.md` |
| `C022` | `commentary` | 新增十篇中文页面属于评论与研究记录。 | 它们不替代原始公理、论文和 PDF 转写。 | `commentary` | `docs/06_commentary/` |

## 回答时的最小格式

先列 `claim_id`，再给结论，再写条件和“不蕴含”。例如：`C011` 支持“存在一个严格混沌构造”；它不支持“已证明本宇宙就是该构造”。如果问题跨越多个层级，同时列出各层命题，不把它们合并为一条无条件推论。
