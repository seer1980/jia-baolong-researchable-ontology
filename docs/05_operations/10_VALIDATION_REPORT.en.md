---
title: "Markdown Theory Archive Validation Report"
author: "Jia Baolong"
lang: "en"
translation_of: "docs/05_operations/10_VALIDATION_REPORT.md"
---

# Markdown Theory Archive Validation Report

Validation date: 2026-08-07

## File Structure

| Item | Count / Result |
|---|---:|
| Total Markdown files | 53 |
| Root-level and `docs/` explanatory files | 14 |
| `papers` full papers | 32 |
| `supplementary_transcriptions` PDF transcriptions | 7 |
| Non-Markdown dependency files | 0 |
| Original paper files modified | 0 |

## Paper Metadata

- All 39 paper files contain YAML metadata, a Zenodo record ID, DOI, `source_kind`, `version_status`, and `authority_tier`.
- 19280200 and 19280552 belong to the same `parallel_group`.

## Structural Review of PDF Transcriptions

| Zenodo ID | PDF pages | Markdown page markers | Display-math blocks | Markdown tables | Result |
|---:|---:|---:|---:|---:|---|
| 19230330 | 29 | 29 | 28 | 8 | PASS |
| 19244836 | 54 | 54 | 0 | 0 | PASS |
| 19245000 | 31 | 31 | 2 | 2 | PASS |
| 19275420 | 13 | 13 | 0 | 0 | PASS |
| 19315010 | 19 | 19 | 0 | 0 | PASS |
| 19317526 | 24 | 24 | 0 | 0 | PASS |
| 19469833 | 32 | 32 | 55 | 9 | PASS |

The total is 202 pages. Page markers are continuous, math delimiters are balanced, and no CMap residue, control character, PDF watermark, or duplicated header/footer was found.

## Markdown and Formulae

Six TeX-derived papers have had their titles, paragraphs, tables, and figure captions organized as Markdown; mathematical content remains in math blocks. Complex formulae in the PDF-reconstructed papers have been restored as LaTeX payloads with superscripts, subscripts, and structural commands.

## Complete Reading Path

`THEORY_READING_GUIDE.md → 00_READ_FIRST.md → docs/01_foundation/ → docs/02_first_beat/ → docs/03_emergence/ → docs/04_reference/ → docs/06_commentary/ → papers/ → supplementary_transcriptions/`

## GitHub Pages Site Output

| Item | Result |
|---|---:|
| HTML pages corresponding to Markdown sources | 53 |
| Total HTML pages, including indexes, search, and 404 | 57 |
| Search-index entries | 53 |
| Sitemap URLs | 56 |
| Broken internal links | 0 |
| Semantic \(`<h1>`\) per page | 1 |
| LaTeX MathJax | configured; all `\[...\]`, `\(...\)`, and `$$...$$` spans protected and restored |
| GitHub Actions Pages workflow | `.github/workflows/pages.yml` |

