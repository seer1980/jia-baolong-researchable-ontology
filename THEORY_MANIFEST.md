# Jia Baolong Theory File Manifest

本文件说明仓库各部分的功能、来源和阅读顺序。论文正文、PDF 全文转写、理论导读和结构化入口分层保存，Markdown 是唯一的理论源文件；`ai/` 提供机器可读索引，`site/` 是由 Markdown 生成的 GitHub Pages HTML 发布目录。

## 文件层级

| 层级 | 位置 | 数量 | 内容 |
|---|---|---:|---|
| `reading_guide` | `THEORY_READING_GUIDE.md`、`00_READ_FIRST.md` | 2 | 完整阅读指南和理论入口 |
| `ai_entry` | `docs/00_ai/` | 8 | 中文入口、术语、命题、关系、版本、测试和阅读协议 |
| `primary_papers` | `papers/` | 32（另有 6 篇英文平行稿） | 论文正文、YAML 元数据和 Zenodo record ID |
| `supplementary_pdf` | `supplementary_transcriptions/` | 7（另有 1 篇英文平行稿） | 按 PDF 页面恢复的全文 |
| `commentary` | 根目录与 `docs/` | 48（含 10 篇新增中文记录） | 理论导读、公式、阅读工具和理解更新 |
| `machine_readable` | `ai/` | 3 个 JSON/JSONL 数据集 | manifest、命题、关系和语义切块 |

## 建议阅读顺序

1. `docs/00_ai/00_AI_START_HERE.md`
2. `docs/00_ai/01_AI_COMPLETE_SYNTHESIS.md`
3. `docs/00_ai/02_AI_CANONICAL_GLOSSARY.md`
4. `docs/00_ai/03_AI_CLAIM_LEDGER.md`
5. `docs/00_ai/04_AI_RELATION_GRAPH.md`
6. `docs/00_ai/05_AI_VERSION_MAP.md`
7. `docs/00_ai/06_AI_COMPREHENSION_TEST.md`
8. `docs/00_ai/07_AI_READING_PROTOCOL.md`
9. `THEORY_READING_GUIDE.md`
10. `00_READ_FIRST.md`
11. `docs/01_foundation/`
12. `docs/02_first_beat/`
13. `docs/03_emergence/`
14. `docs/04_reference/`
15. `docs/05_operations/`
16. `docs/06_commentary/`
17. `papers/`
18. `supplementary_transcriptions/`

## 论文元数据

每篇正文文件保留：

- `zenodo_record_id`
- `concept_record_id`
- `doi`
- `title`
- `publication_date`
- `source_kind`
- `version_status`
- `authority_tier`
- `document_role`
- `parallel_group`（存在版本并行时）

切块时应把这些字段与正文一起保留；检索先返回论文标题、日期、来源和摘要，再返回正文段落。

机器可读层的字段、记录数和中文-only 范围见 `ai/manifest.json`。新增 AI 入口层和此前十篇新增评论与研究记录没有生成对应英文平行稿。

## 数学与文件格式

数学使用 Markdown 数学定界符，LaTeX 只作为公式载体；表格使用 Markdown 表格；PDF 转写保留 `<!-- PDF page N -->` 页面锚点。论文正文、PDF 转写和导读文件均为 UTF-8 Markdown。

## 版本关系

同一 `parallel_group` 的论文属于同一版本族。应按照论文日期、正文内容和理论发展顺序理解其关系，不把不同版本混成一个文本。