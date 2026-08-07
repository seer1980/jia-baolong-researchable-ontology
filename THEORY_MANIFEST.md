# Jia Baolong Theory File Manifest

本文件说明仓库各部分的功能、来源和阅读顺序。论文正文、PDF 全文转写与理论导读分层保存，Markdown 是唯一的理论源文件；`site/` 是由 Markdown 生成的 GitHub Pages HTML 发布目录。

## 文件层级

| 层级 | 位置 | 数量 | 内容 |
|---|---|---:|---|
| `reading_guide` | `THEORY_READING_GUIDE.md`、`00_READ_FIRST.md` | 2 | 完整阅读指南和理论入口 |
| `primary_papers` | `papers/` | 32 | 论文正文、YAML 元数据和 Zenodo record ID |
| `supplementary_pdf` | `supplementary_transcriptions/` | 7 | 按 PDF 页面恢复的全文 |
| `commentary` | 根目录与 `docs/` | 13 | 理论导读、公式、阅读工具和理解更新 |

## 建议阅读顺序

1. `THEORY_READING_GUIDE.md`
2. `00_READ_FIRST.md`
3. `docs/01_foundation/`
4. `docs/02_first_beat/`
5. `docs/03_emergence/`
6. `docs/04_reference/`
7. `docs/05_operations/`
8. `docs/06_commentary/`
9. `papers/`
10. `supplementary_transcriptions/`

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

## 数学与文件格式

数学使用 Markdown 数学定界符，LaTeX 只作为公式载体；表格使用 Markdown 表格；PDF 转写保留 `<!-- PDF page N -->` 页面锚点。论文正文、PDF 转写和导读文件均为 UTF-8 Markdown。

## 版本关系

同一 `parallel_group` 的论文属于同一版本族。应按照论文日期、正文内容和理论发展顺序理解其关系，不把不同版本混成一个文本。
