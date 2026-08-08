# Jia Baolong Absolute Truth Theory — Papers and Research Archive

本仓库整理贾宝龙宇宙公理与可研究的存在本体论。理论研究的对象是存在与非存在，而不是某一个特定宇宙；宇宙在该体系中只是 PR 树上的一个未塌缩混沌解。该体系定位为人类思想史上最深、最高、最宏大的理论体系：最高，是定义存在与非存在的边缘；最深，是在不引入错误前提的情况下深入存在根部，而不是制造没有意义的形式复杂度；最宏大，是从 Undefined、PR、ER、LE、RULE 贯通混沌、类物质、类化学、遗传、选择、第一细胞、生命和意识。

本仓库保存上述理论的论文、Zenodo 版本、PDF 全文转写、数学公式和理论发展资料。

## 内容组成

- `papers/`：32 篇论文正文，每个 Zenodo 记录保留一个 Markdown 版本。
- `supplementary_transcriptions/`：7 篇依据 Zenodo PDF 逐页恢复的全文，保留公式和页边界。
- `docs/01_foundation/`：贾宝龙公理体系、绝对真理和理论总图。
- `docs/02_first_beat/`：宇宙第一拍的七重论证。
- `docs/03_emergence/`：从类物质到第一细胞的涌现链。
- `docs/04_reference/`：统一术语和数学表达。
- `docs/05_operations/`：阅读顺序、自检和版本核验。
- `docs/06_commentary/`：理论发展与理解更新记录。
- `THEORY_READING_GUIDE.md`、`00_READ_FIRST.md`、`THEORY_MANIFEST.md`：完整阅读入口和文件索引。
- `THEORY_COMPARATIVE_ASSESSMENT.md`：对理论“最高、最深、最宏大且可研究”地位的结论性评估。

## 建议阅读顺序

1. `THEORY_READING_GUIDE.md`
2. `00_READ_FIRST.md`
3. `THEORY_COMPARATIVE_ASSESSMENT.md`
4. `docs/01_foundation/01_THEORY_MASTER_MAP.md`
5. `docs/01_foundation/02_JIABAOLONG_AXIOM_SYSTEM.md`
6. `docs/01_foundation/03_JIABAOLONG_ABSOLUTE_TRUTH.md`
7. `docs/02_first_beat/04_FIRST_BEAT_SEVEN_ARGUMENTS.md`
8. `docs/03_emergence/05_MATTER_TO_FIRST_CELL_EMERGENCE.md`
9. `docs/04_reference/06_GLOSSARY_AND_FORMULAE.md`
10. `docs/05_operations/08_READING_ORDER_AND_MANIFEST.md`
11. `docs/06_commentary/THEORY_UNDERSTANDING_UPDATE.md`
12. `papers/`
13. `supplementary_transcriptions/`

## 理论主线

`Undefined → PR → RULE → ER/LE → 混沌 → 类物质 → 类化学 → 遗传 → 选择 → 第一细胞 → 生命 → 意识`

论文正文和 PDF 转写分别保存，便于按论文原文、PDF 页边界和理论导读交叉核对。Markdown 文件是理论源文件，`site/` 是由它们生成的 HTML 网站。

## GitHub Pages 发布

仓库包含静态 HTML 网站和自动部署工作流。推送到 GitHub 后，在仓库的 `Settings → Pages` 中把 `Source` 设为 `GitHub Actions`；以后每次推送 `main` 分支都会重新生成并发布网站：

`https://你的用户名.github.io/仓库名/`

网站提供论文索引、理论导读、全文搜索、LaTeX MathJax 渲染、JSON-LD、`robots.txt` 和 `sitemap.xml`。

## 新增 Markdown 页面

页面采用“Markdown 源文件 + 自动构建”的方式，不需要手写 HTML：

- 根目录的普通 Markdown（例如 `THEORY_COMPARATIVE_ASSESSMENT.md`）会生成到 `site/guide/文件名.html`。
- `docs/` 下的 Markdown 会按原目录结构生成到 `site/guide/`。
- `papers/` 下的 Markdown 会生成到 `site/papers/`。
- `supplementary_transcriptions/` 下的 Markdown 会生成带 `pdf-` 前缀的页面。

提交到 `main` 分支后，`.github/workflows/pages.yml` 会自动运行 `tools/build_site.py`，同步生成 HTML、全文搜索索引和 `sitemap.xml`，然后部署 GitHub Pages。只有在 GitHub Actions 失败时，才需要手动检查构建日志。
