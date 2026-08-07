# Markdown 理论档案验证报告

验证日期：2026-08-07

## 文件结构

| 项目 | 数量/结果 |
|---|---:|
| Markdown 文件总数 | 53 |
| 根目录与 docs/ 说明文件 | 14 |
| papers 论文 | 32 |
| supplementary_transcriptions PDF 转写 | 7 |
| 非 Markdown 依赖文件 | 0 |
| 原始论文文件被修改 | 0 |

## 论文元数据

- 39 篇论文文件均有 YAML 元数据、Zenodo record ID、DOI、source_kind、version_status 和 authority_tier。
- 19280200 与 19280552 具有同一 parallel_group。

## PDF 转写结构复核

| Zenodo ID | PDF 页数 | Markdown 页标 | 展示公式块 | Markdown 表格 | 结果 |
|---:|---:|---:|---:|---:|---|
| 19230330 | 29 | 29 | 28 | 8 | PASS |
| 19244836 | 54 | 54 | 0 | 0 | PASS |
| 19245000 | 31 | 31 | 2 | 2 | PASS |
| 19275420 | 13 | 13 | 0 | 0 | PASS |
| 19315010 | 19 | 19 | 0 | 0 | PASS |
| 19317526 | 24 | 24 | 0 | 0 | PASS |
| 19469833 | 32 | 32 | 55 | 9 | PASS |

合计 202 页。页标连续，公式定界符成对，未发现 CMap 残留、控制字符、PDF 水印或重复页眉页脚。

## Markdown 与公式

六篇 TeX 派生论文已将标题、段落、表格和图注整理为 Markdown，数学内容保留在数学块中。PDF 恢复论文的复杂公式已重建为带上下标和结构命令的 LaTeX 载荷。

## 完整阅读路径

THEORY_READING_GUIDE.md → 00_READ_FIRST.md → docs/01_foundation/ → docs/02_first_beat/ → docs/03_emergence/ → docs/04_reference/ → docs/06_commentary/ → papers/ → supplementary_transcriptions/

## GitHub Pages 网站输出

| 项目 | 结果 |
|---|---:|
| Markdown 源文档对应 HTML 页面 | 53 |
| HTML 总页面数（含索引、搜索和 404） | 57 |
| 搜索索引条目 | 53 |
| sitemap URL | 56 |
| 内部链接断链 | 0 |
| 每页语义 `<h1>` | 1 |
| LaTeX MathJax | 已配置；所有 `\[...\]`、`\(...\)` 和 `$$...$$` 已保护并恢复 |
| GitHub Actions Pages 工作流 | `.github/workflows/pages.yml` |
