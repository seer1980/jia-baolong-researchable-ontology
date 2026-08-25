---
title: "Jia Baolong Theory File Manifest"
author: "Jia Baolong"
lang: "en"
translation_of: "THEORY_MANIFEST.md"
---

# Jia Baolong Theory File Manifest

This file explains the function, provenance, and reading order of each part of the repository. Full papers, PDF transcriptions, and theoretical guides are preserved in layers. Markdown is the sole theory source format; `site/` is the GitHub Pages HTML publication directory generated from Markdown.

## File Hierarchy

| Layer | Location | Count | Contents |
|---|---|---:|---|
| `reading_guide` | `THEORY_READING_GUIDE.md`, `00_READ_FIRST.md` | 2 | Complete reading guide and theory entry point |
| `primary_papers` | `papers/` | 32 | Full papers, YAML metadata, and Zenodo record IDs |
| `supplementary_pdf` | `supplementary_transcriptions/` | 7 | Full texts reconstructed by PDF page |
| `commentary` | root directory and `docs/` | 13 | Theory guides, formulae, reading tools, and updates in understanding |

## Recommended Reading Order

1. `THEORY_READING_GUIDE.en.md`
2. `00_READ_FIRST.en.md`
3. `docs/01_foundation/`
4. `docs/02_first_beat/`
5. `docs/03_emergence/`
6. `docs/04_reference/`
7. `docs/05_operations/`
8. `docs/06_commentary/`
9. `papers/`
10. `supplementary_transcriptions/`

## Paper Metadata

Every full-paper file preserves:

- `zenodo_record_id`
- `concept_record_id`
- `doi`
- `title`
- `publication_date`
- `source_kind`
- `version_status`
- `authority_tier`
- `document_role`
- `parallel_group` (where versions run in parallel)

When documents are chunked, these fields should be retained together with the text. Retrieval should return the paper title, date, source, and abstract before returning body paragraphs.

## Mathematics and File Formats

Mathematics uses Markdown math delimiters, with LaTeX only as the carrier of formulae. Tables use Markdown table syntax. PDF transcriptions preserve page anchors in the form `<!-- PDF page N -->`. Full papers, PDF transcriptions, and guide files are all UTF-8 Markdown.

## Version Relations

Papers in the same `parallel_group` belong to the same version family. Their relation should be understood through publication date, body content, and the sequence of theoretical development; distinct versions must not be blended into a single text.

