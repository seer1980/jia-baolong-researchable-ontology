# Markdown 理论档案验证报告

验证日期：2026-09-07

## 文件结构

| 项目 | 数量/结果 |
|---|---:|
| Markdown 源文件总数（排除 site/、.git/、tools/） | 135 |
| 根目录 Markdown | 15 |
| docs/00_ai 结构化入口 | 8 |
| docs/01_foundation | 6 |
| docs/02_first_beat | 2 |
| docs/03_emergence | 2 |
| docs/04_reference | 2 |
| docs/05_operations | 6 |
| docs/06_commentary | 48（含 10 篇新增中文记录） |
| papers 论文 Markdown | 38（32 篇中文、6 篇英文平行稿） |
| supplementary_transcriptions Markdown | 8（7 篇中文、1 篇英文平行稿） |
| ai/ 机器可读文件 | 4（1 manifest、3 JSONL；构建时复制到 site/ai/） |
| 原始论文正文被修改 | 0 |

## AI 数据层

| 文件 | 记录数 | 校验 |
|---|---:|---|
| ai/manifest.json | 1 个 JSON 对象 | PASS |
| ai/claims.jsonl | 22 | 每行可解析 JSON，PASS |
| ai/relations.jsonl | 20 | 每行可解析 JSON，PASS |
| ai/chunks.jsonl | 22 | 每行可解析 JSON，PASS；覆盖全部 22 条命题 |

`docs/00_ai/` 的八个文件使用中文入口、规范术语、命题、关系、版本、理解测试和阅读协议。新增 AI 入口层以及此前新增的十篇评论与研究记录没有生成英文平行稿；英文论文和已有英文导读保留原状。命题切块覆盖全部 22 条命题，术语切块覆盖规范术语表的 19 个术语。

## 阅读路线与站点生成

完整顺序已同步到 `THEORY_MANIFEST.md` 和 `docs/05_operations/08_READING_ORDER_AND_MANIFEST.md`：先读 AI 入口层，再读规范导读、论文正文和 PDF 转写。`tools/build_site.py` 的首页“AI 专用入口”现在列出八个入口文件和一篇已有深度学习笔记。

| 项目 | 结果 |
|---|---:|
| Markdown 源文档对应 HTML 页面 | 135 |
| HTML 总页面数（含索引、搜索和 404） | 142 |
| 搜索索引条目 | 135 |
| sitemap URL | 139 |
| 首页 AI 入口文件卡片 | 8 |
| 英文站新增 AI 入口页面 | 0（按中文-only 约定） |
| 内部链接断链 | 0（构建器生成路径检查） |
| 每页语义 `<h1>` | 1 |
| LaTeX MathJax | 已配置；公式定界符保护并恢复 |
| GitHub Actions Pages 工作流 | `.github/workflows/pages.yml` |

## 版本与来源检查

- 论文正文、PDF 转写、规范导读、评论记录和 AI 导航层保持分层。
- `source_kind`、`authority_tier`、`document_role` 和 `public_role` 继续用于页面来源标识。
- `ai/claims.jsonl` 中的 `status` 区分 `canonical`、`conditional`、`constructed`、`open`、`interpretive` 和 `commentary`，回答时不得把开放接口改写成已完成证明。
