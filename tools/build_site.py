"""Build a static GitHub Pages site from the repository's Markdown archive."""

from __future__ import annotations

import argparse
import html
import json
import os
import posixpath
import re
import shutil
from pathlib import Path
from typing import Any

import markdown


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "site"
DEFAULT_SITE_BASE_URL = "https://seer1980.github.io/jia-baolong-researchable-ontology"
PUBLIC_TITLE_OVERRIDES = {
    "papers/19448733.md": "A Mathematical Proof of the Origin of the Universe: From Gödel's Theorem to the First Cause",
}


# The public site is ordered by theory structure, not by filesystem spelling.
# Any future guide that is not listed here is still published and is appended to
# an automatically generated "more documents" group.
GUIDE_GROUPS: list[tuple[str, str, list[str]]] = [
    (
        "AI 与读者从这里开始",
        "先建立准确的阅读方法和全局模型，再进入公理、证明与论文细节。",
        [
            "THEORY_READING_GUIDE.md",
            "00_READ_FIRST.md",
        ],
    ),
    (
        "规范理论主线",
        "按零点边界、完整架构、公理、绝对真理、第一实际和向上涌现的顺序阅读。",
        [
            "docs/01_foundation/01_THEORY_MASTER_MAP.md",
            "docs/01_foundation/02_JIABAOLONG_AXIOM_SYSTEM.md",
            "docs/01_foundation/03_JIABAOLONG_ABSOLUTE_TRUTH.md",
            "docs/02_first_beat/04_FIRST_BEAT_SEVEN_ARGUMENTS.md",
            "docs/06_commentary/from-eternal-actual-existence-to-pr-first-beat-necessity.md",
            "docs/03_emergence/05_MATTER_TO_FIRST_CELL_EMERGENCE.md",
            "docs/04_reference/06_GLOSSARY_AND_FORMULAE.md",
            "docs/06_commentary/THEORY_UNDERSTANDING_UPDATE.md",
            "docs/06_commentary/jia-baolong-existence-generation-theory-integrated-understanding.md",
            "docs/06_commentary/existence-undefined-pr-and-comparative-ontology.md",
            "docs/06_commentary/researchable-ontology-2-0-0-research-neighborhood-map.md",
            "docs/06_commentary/jblro-perfection-coherence-and-global-comparison.md",
            "docs/06_commentary/jblro-perfect-theory-retains-imperfection.md",
            "docs/06_commentary/jblro-higher-order-perfection-beyond-naive-perfect-world.md",
            "docs/06_commentary/jia-baolong-theory-system-maturity-quality-report.md",
            "docs/06_commentary/defining-zero-highest-deepest-grandest-elephant-theory.md",
        ],
    ),
    (
        "理论淬火与认识闭环",
        "从极限压力测试进入意识反观，并把唯物主义与唯心主义放回同一生成—认识闭环。",
        [
            "docs/06_commentary/jblro-extreme-stress-test-and-hardening.md",
            "docs/06_commentary/absolute-truth-in-hand-after-reaching-the-boundary-of-thought.md",
            "docs/06_commentary/consciousness-reflects-u-pr-internal-proof-point.md",
            "docs/06_commentary/materialism-and-idealism-in-jblro-generation-loop.md",
            "docs/06_commentary/AI_UNDERSTANDING_AND_AXIOMATIC_ACCEPTANCE.md",
        ],
    ),
    (
        "本体大象与思想史",
        "把历史思想、形式边界和局部科学放回同一整体实在及其生成层级。",
        [
            "ELEPHANT_THEORY_PHENOMENOLOGY_WITH_JIABAOLONG_AXIOMS.md",
            "ELEPHANT_THEORY_CONCEPT.md",
            "docs/06_commentary/jblat-meaningful-absolute-truth-and-godel-boundary.md",
            "THEORY_COMPARATIVE_ASSESSMENT.md",
        ],
    ),
    (
        "维护、核验与授权",
        "文件清单、掌握度检查、构建验证与授权范围。",
        [
            "THEORY_MANIFEST.md",
            "docs/05_operations/08_READING_ORDER_AND_MANIFEST.md",
            "docs/05_operations/09_MASTERY_SELF_CHECK.md",
            "docs/05_operations/10_VALIDATION_REPORT.md",
            "LICENSE_SCOPE.md",
        ],
    ),
]


CURRENT_CORE_PAPERS = [
    "papers/21563153.md",
    "papers/21505212.md",
    "papers/21506792.md",
    "papers/21642863.md",
    "papers/21660081.md",
    "papers/21564664.md",
    "papers/21620492.md",
    "papers/21621264.md",
]


HOMEPAGE_KEYWORDS = [
    "贾宝龙公理体系",
    "贾宝龙绝对真理",
    "Jia Baolong Absolute Truth",
    "JBLAT",
    "可研究本体论",
    "大象理论现象理论",
    "存在生成理论",
    "PR-ER-LE",
]


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    raw = text[4:end].strip("\n")
    body = text[end + len("\n---") :].lstrip("\n")
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value
    return data, body


def first_heading(body: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", body, flags=re.MULTILINE)
    return match.group(1).strip() if match else "贾宝龙绝对真理理论"


def output_path(source: Path) -> Path:
    relative = source.relative_to(ROOT).as_posix()
    # English parallel Markdown is published in a stable /en/ tree.  The
    # language suffix is an authoring detail, not part of the public URL.
    if source.name.endswith(".en.md"):
        base_name = source.name[: -len(".en.md")]
        if relative == "README.en.md":
            return Path("en/index.html")
        if relative.startswith("papers/"):
            return Path("en/papers") / f"{base_name}.html"
        if relative.startswith("supplementary_transcriptions/"):
            return Path("en/papers") / f"pdf-{base_name}.html"
        if relative.startswith("docs/"):
            translated_relative = relative[5 : -len(".en.md")] + ".html"
            return Path("en/guide") / translated_relative
        return Path("en/guide") / f"{base_name}.html"
    if relative == "README.md":
        return Path("index.html")
    if relative.startswith("papers/"):
        return Path("papers") / f"{source.stem}.html"
    if relative.startswith("supplementary_transcriptions/"):
        return Path("papers") / f"pdf-{source.stem}.html"
    if relative.startswith("docs/"):
        return Path("guide") / Path(relative[5:]).with_suffix(".html")
    return Path("guide") / source.with_suffix(".html").name


def relative_url(from_page: Path, to_page: Path) -> str:
    return posixpath.relpath(to_page.as_posix(), from_page.parent.as_posix())


def clean_text(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.DOTALL)
    text = re.sub(r"[`*_>#|]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def shorten(text: str, limit: int = 320) -> str:
    text = clean_text(text)
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def searchable_text(text: str) -> str:
    """Flatten Markdown for full-text search while preserving prose and TeX formulae."""
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    return re.sub(r"\s+", " ", text).strip()


def is_redundant_english_parallel(source: Path) -> bool:
    """Skip an .en.md parallel when its declared source is already English."""
    if not source.name.endswith(".en.md"):
        return False
    meta, _ = parse_frontmatter(source.read_text(encoding="utf-8"))
    translated = meta.get("translation_of", "").strip()
    if not translated:
        return False
    original = ROOT / translated
    if not original.is_file():
        return False
    original_meta, _ = parse_frontmatter(original.read_text(encoding="utf-8"))
    return original_meta.get("language", "").lower().startswith("en")


def public_title(source: Path, title: str) -> str:
    """Return presentation-only title corrections without altering source Markdown."""
    return PUBLIC_TITLE_OVERRIDES.get(source.relative_to(ROOT).as_posix(), title)


def default_base_url() -> str:
    configured = os.environ.get("SITE_BASE_URL", "").strip().rstrip("/")
    if configured:
        return configured
    repository = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if "/" in repository:
        owner, name = repository.split("/", 1)
        if name.lower() == f"{owner}.github.io".lower():
            return f"https://{name}"
        return f"https://{owner}.github.io/{name}"
    # Keep local builds production-correct too. GitHub Actions still derives
    # the URL from GITHUB_REPOSITORY when that variable is available.
    return DEFAULT_SITE_BASE_URL


def repository_url() -> str:
    repository = os.environ.get("GITHUB_REPOSITORY", "").strip()
    return f"https://github.com/{repository}" if repository else ""


def rewrite_markdown_links(rendered: str, source: Path, target: Path) -> str:
    pattern = re.compile(r'(href|src)="([^"]+)"')

    def replace(match: re.Match[str]) -> str:
        attribute, value = match.group(1), match.group(2)
        if value.startswith(("#", "http://", "https://", "mailto:", "data:")):
            return match.group(0)
        path_part, fragment = (value.split("#", 1) + [""])[:2] if "#" in value else (value, "")
        candidate = (source.parent / path_part).resolve()
        try:
            relative_source = candidate.relative_to(ROOT)
        except ValueError:
            return match.group(0)
        if not candidate.exists():
            return match.group(0)
        if path_part.endswith(".md"):
            # An English parallel page should keep readers inside the English
            # tree whenever its linked document has a parallel translation.
            if source.name.endswith(".en.md"):
                english_candidate = candidate.with_name(f"{candidate.stem}.en.md")
                if english_candidate.exists():
                    candidate = english_candidate
            destination = output_path(candidate)
        elif relative_source.as_posix() in {"LICENSE", "LICENSE-CODE"}:
            destination = Path(relative_source.as_posix())
        else:
            return match.group(0)
        new_value = relative_url(target, destination)
        if fragment:
            new_value += f"#{fragment}"
        return f'{attribute}="{html.escape(new_value, quote=True)}"'

    return pattern.sub(replace, rendered)


def page_template(
    *,
    title: str,
    description: str,
    body_html: str,
    target: Path,
    base_url: str,
    source: Path | None = None,
    meta: dict[str, str] | None = None,
    section: str = "guide",
    display_title: str | None = None,
    noindex: bool = False,
    keywords: list[str] | None = None,
    language: str = "zh-CN",
) -> str:
    meta = meta or {}
    keywords = keywords or []
    english = language.startswith("en")
    home_target = Path("en/index.html") if english else Path("index.html")
    search_target = Path("en/search.html") if english else Path("search.html")
    papers_target = Path("en/papers/index.html") if english else Path("papers/index.html")
    home = relative_url(target, home_target)
    search = relative_url(target, search_target)
    papers = relative_url(target, papers_target)
    theory_overview = f'{home}#theory-index'
    styles = relative_url(target, Path("assets/styles.css"))
    script = relative_url(target, Path("assets/search.js"))
    target_posix = target.as_posix()
    if target_posix == "index.html":
        canonical_path = "/"
    elif target_posix.endswith("/index.html"):
        canonical_path = f"/{target_posix[:-len('index.html')]}"
    else:
        canonical_path = f"/{target_posix}"
    canonical = f"{base_url}{canonical_path}"
    alternate_target: Path | None = None
    alternate_language = "zh-CN" if english else "en"
    if source is not None:
        if english and source.name.endswith(".en.md"):
            original_source = source.with_name(source.name.replace(".en.md", ".md"))
            if original_source.exists():
                alternate_target = output_path(original_source)
        elif not english:
            english_source = source.with_name(f"{source.stem}.en.md")
            if english_source.exists():
                alternate_target = output_path(english_source)
    if alternate_target is None:
        paired_indexes = {
            "papers/index.html": Path("en/papers/index.html"),
            "en/papers/index.html": Path("papers/index.html"),
            "search.html": Path("en/search.html"),
            "en/search.html": Path("search.html"),
        }
        alternate_target = paired_indexes.get(target_posix)
    alternate_html = ""
    language_switch = ""
    if alternate_target is not None:
        alternate_url = relative_url(target, alternate_target)
        if alternate_target.as_posix() == "index.html":
            alternate_canonical_path = "/"
        elif alternate_target.as_posix().endswith("/index.html"):
            alternate_canonical_path = f"/{alternate_target.as_posix()[:-len('index.html')]}"
        else:
            alternate_canonical_path = f"/{alternate_target.as_posix()}"
        alternate_html = (
            f'  <link rel="alternate" hreflang="{alternate_language}" '
            f'href="{html.escape(base_url + alternate_canonical_path, quote=True)}">\n'
        )
        language_switch = (
            f'<a href="{html.escape(alternate_url, quote=True)}">'
            f'{"中文" if english else "English"}</a>'
        )
    robots_meta = '  <meta name="robots" content="noindex,follow">\n' if noindex else ""
    keywords_meta = (
        f'  <meta name="keywords" content="{html.escape(", ".join(keywords), quote=True)}">\n'
        if keywords
        else ""
    )
    author = meta.get("author") or "Jia Baolong"
    date = meta.get("publication_date") or meta.get("date") or ""
    source_links: list[str] = []
    if source is not None:
        source_url = repository_url()
        if source_url:
            source_links.append(
                f'<a href="{source_url}/blob/main/{source.relative_to(ROOT).as_posix()}">GitHub Markdown 原文</a>'
            )
    if meta.get("zenodo_url"):
        source_links.append(f'<a href="{html.escape(meta["zenodo_url"], quote=True)}">Zenodo record</a>')
    if meta.get("doi"):
        doi = meta["doi"]
        doi_url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
        source_links.append(f'<a href="{html.escape(doi_url, quote=True)}">DOI</a>')
    meta_html = ""
    if source_links or author or date:
        bits = [f"<span>{html.escape(author)}</span>"]
        if date:
            bits.append(f"<span>{html.escape(date)}</span>")
        bits.extend(source_links)
        meta_html = '<div class="page-meta">' + " · ".join(bits) + "</div>"
    json_ld: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle" if section == "paper" else "WebPage",
        "name": title,
        "headline": title,
        "description": description,
        "url": canonical,
    }
    if keywords:
        json_ld["keywords"] = keywords
        json_ld["about"] = [{"@type": "Thing", "name": keyword} for keyword in keywords]
    visible_title = render_title(display_title or title)
    breadcrumbs = "" if target_posix in {"index.html", "en/index.html"} else (
        f'    <div class="breadcrumbs"><a href="{home}">{"Home" if english else "首页"}</a> '
        f'<span>›</span> <span>{html.escape(section)}</span></div>'
    )
    if section == "paper":
        json_ld["author"] = {"@type": "Person", "name": author}
        if date:
            json_ld["datePublished"] = date
        if meta.get("doi"):
            json_ld["sameAs"] = f"https://doi.org/{meta['doi']}"
    return f'''<!doctype html>
<html lang="{html.escape(language, quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · Jia Baolong Researchable Ontology</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
{robots_meta}{keywords_meta}  <link rel="canonical" href="{html.escape(canonical, quote=True)}">
{alternate_html}  <link rel="stylesheet" href="{styles}">
  <script>window.MathJax = {{loader: {{load: ['[tex]/mathtools', '[tex]/centernot']}}, tex: {{packages: {{'[+]': ['mathtools', 'centernot']}}, macros: {{outdeg: '\\\\operatorname{{outdeg}}', indeg: '\\\\operatorname{{indeg}}', totdeg: '\\\\operatorname{{totdeg}}'}}, inlineMath: [['\\\\(', '\\\\)'], ['$', '$']], displayMath: [['\\\\[', '\\\\]'], ['$$', '$$']]}}, options: {{skipHtmlTags: ['script','noscript','style','textarea','pre','code']}}}};</script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <script defer src="{script}"></script>
  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="{home}">{"Jia Baolong Axiom System" if english else "贾宝龙公理体系"}</a>
      <nav aria-label="{'Primary navigation' if english else '主导航'}"><a href="{home}">{"Home" if english else "首页"}</a><a href="{theory_overview}">{"Theory" if english else "理论总览"}</a><a href="{papers}">{"Papers" if english else "论文"}</a><a href="{search}">{"Search" if english else "搜索"}</a>{language_switch}</nav>
    </div>
  </header>
  <main class="page-shell">
{breadcrumbs}
    <article class="document">
      <h1>{visible_title}</h1>
      {meta_html}
      <div class="document-body">{body_html}</div>
    </article>
  </main>
  <footer class="site-footer"><a href="{home}">{"Jia Baolong Axiom System and Researchable Ontology" if english else "贾宝龙公理体系与可研究本体论"}</a><span>{"Full Markdown · HTML site" if english else "Markdown 全文 · HTML 网站"}</span></footer>
</body>
</html>
'''


def normalize_text_latex(body: str) -> str:
    """Remove print-only LaTeX commands left outside protected math spans."""
    body = re.sub(r"(?m)^[ \t]*\\newpage[ \t]*(?:\n|$)", "", body)
    body = re.sub(
        r"\\multirow\{[^{}]*\}\{[^{}]*\}\{([^{}]*)\}",
        lambda match: match.group(1).replace(r"\%", "%"),
        body,
    )
    body = re.sub(
        r"\\cite\{([^{}]+)\}",
        lambda match: "[" + "; ".join(key.strip() for key in match.group(1).split(",")) + "]",
        body,
    )
    return body.replace(r"\textless", "<").replace(r"\textgreater", ">")


def render_markdown(body: str) -> str:
    protected, replacements = protect_math(body)
    protected = normalize_text_latex(protected)
    rendered = markdown.markdown(
        protected,
        extensions=["extra", "tables", "fenced_code", "toc", "sane_lists"],
        output_format="html5",
    )
    for token, formula, display in replacements:
        escaped_formula = html.escape(formula, quote=False)
        wrapper = (
            f'<div class="math-block">{escaped_formula}</div>'
            if display
            else f'<span class="math-inline">{escaped_formula}</span>'
        )
        rendered = rendered.replace(f"<p>{token}</p>", wrapper)
        rendered = rendered.replace(token, wrapper)
    return rendered


def render_title(title: str) -> str:
    """Render inline TeX in a page title without letting Markdown alter it."""
    protected, replacements = protect_math(title)
    rendered = html.escape(protected, quote=False)
    for token, formula, _display in replacements:
        rendered = rendered.replace(token, f'<span class="math-inline">{html.escape(formula, quote=False)}</span>')
    return rendered


def protect_math(body: str) -> tuple[str, list[tuple[str, str, bool]]]:
    """Protect TeX delimiters from Markdown's backslash and emphasis parsing."""
    pattern = re.compile(
        r"\\\[(.*?)\\\]"      # \[ ... \]
        r"|\$\$(.*?)\$\$"      # $$ ... $$
        r"|\\\((.*?)\\\)"      # \( ... \)
        r"|(?<!\$)\$(?!\$)(.+?)(?<!\$)\$",
        flags=re.DOTALL,
    )
    replacements: list[tuple[str, str, bool]] = []

    def replace(match: re.Match[str]) -> str:
        if match.group(1) is not None:
            formula, display = f"\\[{match.group(1)}\\]", True
        elif match.group(2) is not None:
            formula, display = f"$${match.group(2)}$$", True
        elif match.group(3) is not None:
            formula, display = f"\\({match.group(3)}\\)", False
        else:
            formula, display = f"${match.group(4)}$", False
        token = f"MATHTOKEN{len(replacements):05d}END"
        replacements.append((token, formula, display))
        return token

    return pattern.sub(replace, body), replacements


def strip_first_h1(rendered: str) -> str:
    """Use the template's semantic h1 and keep the source heading hierarchy below it."""
    return re.sub(r"^\s*<h1[^>]*>.*?</h1>\s*", "", rendered, count=1, flags=re.DOTALL)


def write_page(output_root: Path, target: Path, content: str) -> None:
    destination = output_root / target
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def redirect_page(*, title: str, destination: str, language: str = "en") -> str:
    """Create a noindex compatibility page for a retired public URL."""
    escaped_title = html.escape(title)
    escaped_destination = html.escape(destination, quote=True)
    return f'''<!doctype html>
<html lang="{html.escape(language, quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,follow">
  <meta http-equiv="refresh" content="0; url={escaped_destination}">
  <link rel="canonical" href="{escaped_destination}">
  <title>{escaped_title}</title>
</head>
<body>
  <p>This page has moved permanently to <a href="{escaped_destination}">{escaped_title}</a>.</p>
</body>
</html>
'''


def build(output_root: Path) -> None:
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    base_url = default_base_url()
    repo_url = repository_url()
    entries: list[dict[str, Any]] = []
    readme_rendered = ""
    readme_meta: dict[str, str] = {}
    english_readme_rendered = ""
    english_readme_meta: dict[str, str] = {}
    source_files = [
        source
        for source in sorted(
        p
        for p in ROOT.rglob("*.md")
        if "site" not in p.relative_to(ROOT).parts
        and ".git" not in p.relative_to(ROOT).parts
        and "tools" not in p.relative_to(ROOT).parts
        )
        if not is_redundant_english_parallel(source)
    ]
    for source in source_files:
        relative = source.relative_to(ROOT)
        text = source.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        title = meta.get("title") or first_heading(body)
        title = public_title(source, title)
        if relative.as_posix() == "README.md":
            title = "贾宝龙公理体系与可研究本体论"
        elif relative.as_posix() == "README.en.md":
            title = "Jia Baolong Axiom System and Researchable Ontology"
        display_title = title if relative.as_posix() in {"README.md", "README.en.md"} else first_heading(body)
        description = shorten(body, 260)
        section = "paper" if relative.parts[0] in {"papers", "supplementary_transcriptions"} else "guide"
        language = "en" if source.name.endswith(".en.md") or meta.get("language", "").lower().startswith("en") else "zh-CN"
        target = output_path(source)
        rendered = strip_first_h1(rewrite_markdown_links(render_markdown(body), source, target))
        if relative.as_posix() == "README.md":
            readme_rendered = rendered
            readme_meta = meta
        elif relative.as_posix() == "README.en.md":
            english_readme_rendered = rendered
            english_readme_meta = meta
        content = page_template(
            title=title,
            description=description,
            body_html=rendered,
            target=target,
            base_url=base_url,
            source=source,
            meta=meta,
            section=section,
            display_title=display_title,
            language=language,
        )
        write_page(output_root, target, content)
        entries.append(
            {
                "title": title,
                "description": description,
                "content": searchable_text(body),
                "source": relative.as_posix(),
                "url": target.as_posix(),
                "section": section,
                "author": meta.get("author", "Jia Baolong"),
                "date": meta.get("publication_date", ""),
                "zenodo_url": meta.get("zenodo_url", ""),
                "doi": meta.get("doi", ""),
                "language": language,
                "parallel": source.name.endswith(".en.md"),
                "keywords": " ".join(
                    filter(
                        None,
                        [title, meta.get("author", ""), meta.get("document_role", ""), relative.stem]
                        + (HOMEPAGE_KEYWORDS if relative.as_posix() == "README.md" else []),
                    )
                ),
            }
        )

    # The Chinese archive keeps source records in their original positions;
    # English parallel sources belong only to the English navigation tree.
    papers = [entry for entry in entries if entry["section"] == "paper" and not entry["parallel"]]
    guides = [entry for entry in entries if entry["section"] == "guide" and not entry["parallel"]]
    english_entries = [entry for entry in entries if entry["language"] == "en"]
    english_papers = [entry for entry in english_entries if entry["section"] == "paper"]
    english_guides = [entry for entry in english_entries if entry["section"] == "guide" and entry["source"] != "README.en.md"]
    entries_by_source = {entry["source"]: entry for entry in entries}

    def listing_title(entry: dict[str, Any]) -> str:
        return re.sub(r"[*_`]", "", entry["title"]).strip()

    def directory_items(items: list[dict[str, Any]], target: Path) -> str:
        rows: list[str] = []
        for entry in items:
            href = relative_url(target, Path(entry["url"]))
            record_id = Path(entry["source"]).stem
            if entry["source"].startswith("supplementary_transcriptions/"):
                detail = f"PDF 全文恢复 · Zenodo {record_id}"
            else:
                detail = entry["date"] or f"Zenodo {record_id}"
            rows.append(
                f'<li><a href="{html.escape(href, quote=True)}">{html.escape(listing_title(entry))}</a>'
                f'<span>{html.escape(detail)}</span></li>'
            )
        return "".join(rows)

    def content_cards(items: list[dict[str, Any]], target: Path) -> str:
        cards: list[str] = []
        for entry in items:
            href = relative_url(target, Path(entry["url"]))
            cards.append(
                f'<article class="content-card"><h3><a href="{html.escape(href, quote=True)}">'
                f'{html.escape(listing_title(entry))}</a></h3>'
                f'<p>{html.escape(shorten(entry["description"], 150))}</p></article>'
            )
        return '<div class="content-grid">' + "".join(cards) + "</div>"

    paper_entries = [entry for entry in papers if entry["source"].startswith("papers/")]
    pdf_entries = [entry for entry in papers if entry["source"].startswith("supplementary_transcriptions/")]
    core_papers = [entries_by_source[source] for source in CURRENT_CORE_PAPERS if source in entries_by_source]
    core_sources = {entry["source"] for entry in core_papers}
    historical_papers = [entry for entry in paper_entries if entry["source"] not in core_sources]
    papers_body = f'''<p class="lead">全部 32 篇论文正文和 7 篇 PDF 全文恢复均原样保留。默认先读当前核心论文，再按 Zenodo 记录顺序查看理论发展档案。</p>
<h2>当前核心论文</h2>
<p>根部边界、绝对真理、第一实际、反向追溯、意识与自指的当前核心论证。</p>
<ul class="directory-list">{directory_items(core_papers, Path("papers/index.html"))}</ul>
<h2>理论发展档案</h2>
<p>以下论文按 Zenodo 记录号从早到晚排列，用于研究理论的形成与收束过程。</p>
<ul class="directory-list">{directory_items(historical_papers, Path("papers/index.html"))}</ul>
<h2>PDF 全文恢复</h2>
<p>依据 Zenodo PDF 逐页恢复的 Markdown 全文，保留公式与页边界。</p>
<ul class="directory-list">{directory_items(pdf_entries, Path("papers/index.html"))}</ul>'''

    def english_directory_items(items: list[dict[str, Any]], target: Path) -> str:
        rows: list[str] = []
        for entry in items:
            href = relative_url(target, Path(entry["url"]))
            record_id = Path(entry["source"]).stem.removesuffix(".en")
            detail = (
                f"PDF transcription · Zenodo {record_id}"
                if entry["source"].startswith("supplementary_transcriptions/")
                else entry["date"] or f"Zenodo {record_id}"
            )
            rows.append(
                f'<li><a href="{html.escape(href, quote=True)}">{html.escape(listing_title(entry))}</a>'
                f'<span>{html.escape(detail)}</span></li>'
            )
        return "".join(rows)

    english_home_body = fr'''<section class="theory-hero">
<p class="eyebrow">Jia Baolong Axiom System · Researchable Ontology</p>
<p class="hero-claim">A researchable account of existence and nonexistence: from the Undefined boundary and PR to emergence, life, consciousness, and self-recognition.</p>
<p>The Jia Baolong Axiom System does not study one particular universe. It defines the boundary from which positive ontology can begin, treats PR as the first actual face, and places chaos, proto-matter, life, consciousness, and existence recognizing itself on one researchable generative chain.</p>
<div class="theory-chain math-block">$$
U_*\mid\mathrm{{PR}}
\to\mathrm{{ER+LE}}
\xRightarrow{{\mathrm{{RULE}}}}\mathrm{{Chaos}}
\to\mathrm{{ProtoMatter}}
\to\mathrm{{Life}}
\to\mathrm{{Consciousness}}
\to\operatorname{{Recognize}}(U_*\mid\mathrm{{PR}})
$$</div>
<div class="hero-actions"><a class="button primary" href="#english-theory-index">Read the theory</a><a class="button" href="search.html">Search English full text</a><a class="button" href="papers/index.html">Browse English papers</a></div>
</section>
<section class="semantic-identity" aria-labelledby="english-theory-names">
<h2 id="english-theory-names">Names of the theory and their relation</h2>
<dl class="term-map">
<div><dt>Jia Baolong Axiom System</dt><dd>The formal foundation for existence and nonexistence, dynamic actuality, PR, ER, LE, and concrete RULE.</dd></div>
<div><dt>Jia Baolong Absolute Truth (JBLAT)</dt><dd>The Undefined boundary, expressed as “even no nonbeing,” that fixes the zero point from which positive ontology begins.</dd></div>
<div><dt>Researchable Ontology</dt><dd>A program that specifies investigable interfaces among the first actual, concrete generation, chaos, proto-matter, life, and consciousness.</dd></div>
<div><dt>Elephant Theory / Phenomenology</dt><dd>The phenomenological layer examining how finite observers, intellectual history, and disciplines disclose the same whole ontology from partial or remote positions.</dd></div>
</dl>
</section>
<section class="home-section" id="english-theory-index"><h2>English theory documents</h2>
<p>Parallel English editions preserve the definitions, arguments, mathematical notation, and research structure of the Chinese archive.</p>
{content_cards(english_guides, Path("en/index.html"))}</section>
<section class="home-section corpus-entry"><h2>English papers and search</h2>
<p>The English archive contains parallel editions of Chinese-primary papers and source documents that were already written in English.</p>
<div class="hero-actions"><a class="button primary" href="papers/index.html">English paper index</a><a class="button" href="search.html">Search English full text</a></div></section>
<details class="archive-panel repository-notes"><summary>Repository notes</summary>{english_readme_rendered}</details>'''

    english_papers_body = f'''<p class="lead">English editions and English-original papers in the Jia Baolong Axiom System archive. Mathematical expressions remain in LaTex notation for exact rendering and machine reading.</p>
<h2>English papers</h2>
<ul class="directory-list">{english_directory_items(english_papers, Path("en/papers/index.html"))}</ul>'''

    used_guide_sources = {"README.md"}
    guide_sections: list[str] = []
    for heading, introduction, sources in GUIDE_GROUPS:
        group_entries = [entries_by_source[source] for source in sources if source in entries_by_source]
        used_guide_sources.update(entry["source"] for entry in group_entries)
        cards = content_cards(group_entries, Path("index.html"))
        if heading == "维护、核验与授权":
            guide_sections.append(
                f'<details class="archive-panel"><summary>{html.escape(heading)}</summary>'
                f'<p>{html.escape(introduction)}</p>{cards}</details>'
            )
        else:
            guide_sections.append(
                f'<section class="home-section"><h2>{html.escape(heading)}</h2>'
                f'<p>{html.escape(introduction)}</p>{cards}</section>'
            )

    unlisted_guides = [entry for entry in guides if entry["source"] not in used_guide_sources]
    if unlisted_guides:
        guide_sections.append(
            '<section class="home-section"><h2>更多理论文档</h2>'
            '<p>自动收录尚未加入规范顺序的新文档，确保任何 Markdown 页面都不会从网站入口消失。</p>'
            f'{content_cards(unlisted_guides, Path("index.html"))}</section>'
        )

    home_body = fr'''<section class="theory-hero">
<p class="eyebrow">Jia Baolong Axiom System · Researchable Ontology</p>
<p class="hero-claim">从贾宝龙绝对真理到第一实际、生命、意识与大象理论现象理论。</p>
<p>贾宝龙公理体系与可研究本体论研究存在与非存在，而不是某一个具体宇宙。体系以 $U$ 定义全部正面本体论得以开始的零点，以 PR 表达第一实际面，并把混沌、类物质、生命、意识和存在对自身的认识纳入同一条可继续研究的生成链。</p>
<div class="theory-chain math-block">$$
U_*\mid\mathrm{{PR}}
\to\mathrm{{ER+LE}}
\xRightarrow{{\mathrm{{RULE}}}}\mathrm{{Chaos}}
\to\mathrm{{ProtoMatter}}
\to\mathrm{{Life}}
\to\mathrm{{Consciousness}}
\to\operatorname{{Recognize}}(U_*\mid\mathrm{{PR}})
$$</div>
<div class="hero-actions"><a class="button primary" href="#theory-index">按规范顺序阅读</a><a class="button" href="search.html">搜索全部正文</a><a class="button" href="papers/index.html">查看论文档案</a></div>
</section>
<section class="semantic-identity" aria-labelledby="theory-names">
<h2 id="theory-names">理论名称及其统一关系</h2>
<dl class="term-map">
<div><dt>贾宝龙公理体系</dt><dd>规定存在与非存在、动态实际、PR、ER、LE 与具体 RULE 的形式基础。</dd></div>
<div><dt>贾宝龙绝对真理（JBLAT）</dt><dd>以“连无都无”的 $U$ 定义零正面本体边界，固定全部正面本体论得以开始的零点。</dd></div>
<div><dt>可研究本体论</dt><dd>不止描述本原，而是给出第一实际、具体生成、混沌、类物质、生命和意识之间可继续计算、模拟与分层研究的接口。</dd></div>
<div><dt>大象理论现象理论</dt><dd>作为体系的现象理论层，研究有限观察者、历史思想和不同学科怎样从局部或远程位置显现同一整体本体。</dd></div>
</dl>
</section>
<section class="claim-grid" aria-label="理论定位">
<article><h2>最高</h2><p>定义存在与非存在得以被规定的边缘。</p></article>
<article><h2>最深</h2><p>剥除全部正面预设，抵达“连无都无”的零点根部。</p></article>
<article><h2>最宏大</h2><p>覆盖第一实际、可能分支、物质、生命、意识与思想史。</p></article>
</section>
<div id="theory-index" class="theory-index">{"".join(guide_sections)}</div>
<section class="home-section corpus-entry"><h2>完整论文与搜索</h2>
<p>理论总览负责建立准确阅读顺序；论文档案保留全部原始正文和 PDF 恢复稿；全文搜索用于直接定位概念、公式和论证。</p>
<div class="hero-actions"><a class="button primary" href="papers/index.html">进入论文全文索引</a><a class="button" href="search.html">全文搜索</a></div></section>
<details class="archive-panel repository-notes"><summary>仓库结构与发布说明</summary>{readme_rendered}</details>'''

    write_page(
        output_root,
        Path("index.html"),
        page_template(
            title="贾宝龙公理体系与可研究本体论",
            description="贾宝龙公理体系以贾宝龙绝对真理 JBLAT 定义连无都无的零点边界，建立从第一实际到生命、意识与大象理论现象理论的可研究本体论。",
            body_html=home_body,
            target=Path("index.html"),
            base_url=base_url,
            source=ROOT / "README.md",
            meta=readme_meta,
            section="home",
            display_title="贾宝龙公理体系与可研究本体论",
            keywords=HOMEPAGE_KEYWORDS,
        ),
    )
    write_page(
        output_root,
        Path("en/index.html"),
        page_template(
            title="Jia Baolong Axiom System and Researchable Ontology",
            description="An English research archive for the Jia Baolong Axiom System, JBLAT, the PR–ER–LE framework, emergence, consciousness, and Elephant Theory phenomenology.",
            body_html=english_home_body,
            target=Path("en/index.html"),
            base_url=base_url,
            source=ROOT / "README.en.md",
            meta=english_readme_meta,
            section="home",
            display_title="Jia Baolong Axiom System and Researchable Ontology",
            keywords=[
                "Jia Baolong Axiom System",
                "Jia Baolong Absolute Truth",
                "JBLAT",
                "Researchable Ontology",
                "PR ER LE",
                "Elephant Theory",
            ],
            language="en",
        ),
    )

    guides_body = '''<p class="lead">理论导读已经合并到网站主页，并按规范阅读顺序分组。所有原有文章地址保持不变。</p>
<p><a class="button primary" href="../index.html#theory-index">前往主页理论总览</a></p>'''
    write_page(
        output_root,
        Path("papers/index.html"),
        page_template(
            title="论文全文索引",
            description="贾宝龙公理体系与可研究本体论的论文正文及 PDF 全文恢复索引。",
            body_html=papers_body,
            target=Path("papers/index.html"),
            base_url=base_url,
            section="papers",
        ),
    )
    write_page(
        output_root,
        Path("en/papers/index.html"),
        page_template(
            title="English Paper Index",
            description="English editions and English-original papers from the Jia Baolong Axiom System archive.",
            body_html=english_papers_body,
            target=Path("en/papers/index.html"),
            base_url=base_url,
            section="papers",
            language="en",
        ),
    )
    write_page(
        output_root,
        Path("guide/index.html"),
        page_template(
            title="理论总览已合并到主页",
            description="旧理论导读入口保留用于兼容；规范理论索引已合并到网站主页。",
            body_html=guides_body,
            target=Path("guide/index.html"),
            base_url=base_url,
            section="guide",
            noindex=True,
        ),
    )
    write_page(
        output_root,
        Path("search.html"),
        page_template(
            title="全文搜索",
            description="搜索贾宝龙公理体系、贾宝龙绝对真理、可研究本体论及其论文、公式和理论导读。",
            body_html='''<section class="search-panel"><label for="search-input">搜索论文、公式和理论概念</label><div class="search-row"><input id="search-input" type="search" placeholder="例如：PR、Undefined、第一拍、类物质、Rule 979" autocomplete="off"><button id="search-button" type="button">搜索</button></div><p id="search-status" class="search-status">正在加载全文索引…</p><div id="search-results" class="search-results" aria-live="polite"></div></section>''',
            target=Path("search.html"),
            base_url=base_url,
            section="search",
        ),
    )
    write_page(
        output_root,
        Path("en/search.html"),
        page_template(
            title="English Full-Text Search",
            description="Search English editions of the Jia Baolong Axiom System archive, including papers, formulas, and theory documents.",
            body_html='''<section class="search-panel"><label for="search-input">Search English papers, formulas, and theory concepts</label><div class="search-row"><input id="search-input" type="search" placeholder="For example: PR, Undefined, first beat, proto-matter, Rule 979" autocomplete="off"><button id="search-button" type="button">Search</button></div><p id="search-status" class="search-status">Loading the English full-text index…</p><div id="search-results" class="search-results" aria-live="polite"></div></section>''',
            target=Path("en/search.html"),
            base_url=base_url,
            section="search",
            language="en",
        ),
    )
    write_page(
        output_root,
        Path("404.html"),
        page_template(
            title="页面未找到",
            description="请求的页面不存在。",
            body_html='<p class="lead">页面不存在，请返回<a href="index.html">首页</a>或使用<a href="search.html">全文搜索</a>。</p>',
            target=Path("404.html"),
            base_url=base_url,
            section="404",
        ),
    )
    moved_paper_title = PUBLIC_TITLE_OVERRIDES["papers/19448733.md"]
    moved_paper_url = f"{base_url}/papers/19448733.html"
    write_page(
        output_root,
        Path("en/papers/19448733.html"),
        redirect_page(title=moved_paper_title, destination=moved_paper_url),
    )

    assets = output_root / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "styles.css").write_text(STYLES_CSS, encoding="utf-8")
    (assets / "search.js").write_text(SEARCH_JS, encoding="utf-8")
    (output_root / "search.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    english_search_entries: list[dict[str, Any]] = []
    for entry in english_entries:
        english_entry = dict(entry)
        english_entry["url"] = relative_url(Path("en/search.html"), Path(entry["url"]))
        english_search_entries.append(english_entry)
    (output_root / "en" / "search.json").write_text(
        json.dumps(english_search_entries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (output_root / ".nojekyll").write_text("", encoding="utf-8")
    for filename in ("LICENSE", "LICENSE-CODE"):
        shutil.copyfile(ROOT / filename, output_root / filename)
    sitemap_urls = [
        f"{base_url}/"
        if entry["url"] == "index.html"
        else f"{base_url}/en/"
        if entry["url"] == "en/index.html"
        else f"{base_url}/{entry['url']}"
        for entry in entries
    ]
    sitemap_urls.extend([f"{base_url}/papers/", f"{base_url}/search.html", f"{base_url}/en/papers/", f"{base_url}/en/search.html"])
    sitemap = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
    sitemap += "".join(f"  <url><loc>{html.escape(url)}</loc></url>\n" for url in sorted(set(sitemap_urls)))
    sitemap += "</urlset>\n"
    (output_root / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    robots = f"User-agent: *\nAllow: /\n\nSitemap: {base_url}/sitemap.xml\n"
    (output_root / "robots.txt").write_text(robots, encoding="utf-8")
    (output_root / "site-config.json").write_text(
        json.dumps({"base_url": base_url, "github_repository": repo_url, "source_markdown_count": len(source_files)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


STYLES_CSS = r'''
:root{--ink:#132238;--muted:#5c6b7c;--line:#dbe3ec;--paper:#ffffff;--wash:#f4f7fb;--accent:#1264a3;--accent-dark:#0b4778;--warm:#f0b44d;}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--wash);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.72}.site-header{background:#0e2238;color:#fff;border-bottom:4px solid var(--warm)}.header-inner{max-width:1180px;margin:auto;padding:1rem 1.25rem;display:flex;align-items:center;justify-content:space-between;gap:1.5rem}.brand{color:#fff;text-decoration:none;font-weight:760;letter-spacing:.02em}.site-header nav{display:flex;gap:1rem;flex-wrap:wrap}.site-header nav a{color:#d8e9f7;text-decoration:none;font-size:.92rem}.site-header nav a:hover{color:#fff}.page-shell{max-width:1040px;margin:0 auto;padding:1.25rem 1.1rem 4rem}.breadcrumbs{color:var(--muted);font-size:.88rem;margin:.25rem 0 1rem}.breadcrumbs a{color:var(--accent)}.document{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:clamp(1.2rem,3vw,3rem);box-shadow:0 12px 38px rgba(22,47,76,.07)}h1,h2,h3,h4{line-height:1.24;color:var(--ink)}h1{font-size:clamp(1.9rem,4.5vw,3.1rem);margin:.1rem 0 .6rem}h2{margin-top:2.3rem;border-bottom:1px solid var(--line);padding-bottom:.35rem}h3{margin-top:1.6rem}.page-meta{display:flex;flex-wrap:wrap;gap:.35rem .8rem;color:var(--muted);font-size:.9rem;padding:.55rem 0 1.35rem;border-bottom:1px solid var(--line)}.page-meta a{color:var(--accent)}.document-body{font-size:1.02rem}.document-body a{color:var(--accent-dark)}.document-body img{max-width:100%;height:auto}.document-body blockquote{border-left:4px solid var(--warm);background:#fff8e9;margin:1.2rem 0;padding:.65rem 1rem;color:#37465a}.document-body pre{overflow:auto;background:#142436;color:#eaf3fb;padding:1rem;border-radius:10px}.document-body code{background:#eef3f8;padding:.12rem .3rem;border-radius:4px}.document-body pre code{background:transparent;padding:0}.document-body table{border-collapse:collapse;display:block;overflow:auto;width:100%;margin:1rem 0}.document-body th,.document-body td{border:1px solid var(--line);padding:.5rem .7rem;text-align:left;vertical-align:top}.document-body th{background:#edf4fa}.document-body .math-block{text-align:center;overflow:auto}.lead{font-size:1.12rem;color:#344963}.directory-list{list-style:none;padding:0;margin:1rem 0}.directory-list li{display:flex;justify-content:space-between;gap:1rem;border-bottom:1px solid var(--line);padding:.72rem .2rem}.directory-list li span{color:var(--muted);font-size:.88rem;text-align:right}.search-panel{max-width:800px;margin:0 auto}.search-panel label{display:block;font-weight:700;margin-bottom:.45rem}.search-row{display:flex;gap:.6rem}.search-row input{flex:1;border:1px solid #aebdcd;border-radius:8px;padding:.75rem .85rem;font:inherit}.search-row button{border:0;border-radius:8px;padding:.75rem 1.2rem;background:var(--accent);color:#fff;font:inherit;font-weight:700;cursor:pointer}.search-row button:hover{background:var(--accent-dark)}.search-status{color:var(--muted);font-size:.92rem}.search-result{border-top:1px solid var(--line);padding:1rem 0}.search-result h3{margin:0 0 .2rem}.search-result p{margin:.25rem 0;color:#41546b}.result-meta{font-size:.82rem;color:var(--muted)}.site-footer{max-width:1040px;margin:auto;padding:1.25rem 1.1rem 3rem;display:flex;justify-content:space-between;gap:1rem;color:var(--muted);font-size:.86rem}.site-footer a{color:var(--accent)}.theory-hero{margin:1rem 0 2rem;padding:clamp(1.25rem,3vw,2.25rem);border-radius:14px;background:linear-gradient(135deg,#102943,#174c70);color:#edf7ff}.theory-hero p{max-width:850px}.theory-hero .eyebrow{margin:0;color:#f4c86f;font-size:.82rem;font-weight:800;letter-spacing:.13em;text-transform:uppercase}.theory-hero .hero-claim{font-size:clamp(1.18rem,2.3vw,1.55rem);line-height:1.48;font-weight:720}.theory-hero .math-block{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);border-radius:10px;padding:.55rem;margin:1.25rem 0;color:#fff}.hero-actions{display:flex;flex-wrap:wrap;gap:.7rem;margin:1.25rem 0 .2rem}.document-body .button{display:inline-block;border:1px solid #8ba6bd;border-radius:8px;padding:.62rem .95rem;color:#163a56;text-decoration:none;font-weight:720;background:#fff}.document-body .button.primary{border-color:var(--accent);background:var(--accent);color:#fff}.theory-hero .button{border-color:#bed0df;color:#163a56}.theory-hero .button.primary{border-color:#f0b44d;background:#f0b44d;color:#172638}.semantic-identity{margin:2.2rem 0}.term-map{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.85rem;margin:1rem 0}.term-map>div{border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:9px;padding:.85rem 1rem;background:#f8fbfe}.term-map dt{font-weight:780;color:#193a55}.term-map dd{margin:.3rem 0 0;color:#4c5f73;font-size:.94rem}.claim-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;margin:1.5rem 0 2.5rem}.claim-grid article{border:1px solid var(--line);border-top:4px solid var(--warm);border-radius:12px;padding:1rem;background:#f9fbfd}.claim-grid h2{border:0;margin:0 0 .35rem;padding:0;font-size:1.22rem}.claim-grid p{margin:0;color:#40536a}.theory-index{scroll-margin-top:1rem}.home-section{margin-top:2.8rem}.content-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.85rem;margin:1rem 0}.content-card{border:1px solid var(--line);border-radius:10px;padding:1rem;background:#fbfdff}.content-card h3{font-size:1.02rem;margin:0 0 .45rem}.content-card h3 a{text-decoration:none}.content-card p{margin:0;color:#526276;font-size:.92rem;line-height:1.55}.archive-panel{margin:2.2rem 0;border:1px solid var(--line);border-radius:10px;background:#f8fafc;padding:.85rem 1rem}.archive-panel summary{cursor:pointer;font-weight:760;color:#243b53}.archive-panel[open] summary{margin-bottom:.8rem}.repository-notes .document-body{font-size:.95rem}.corpus-entry{border-top:2px solid var(--line);padding-top:.3rem}@media(max-width:680px){.header-inner{display:block}.site-header nav{margin-top:.7rem}.directory-list li{display:block}.directory-list li span{display:block;text-align:left;margin-top:.2rem}.claim-grid,.content-grid,.term-map{grid-template-columns:1fr}.theory-hero{padding:1.1rem}.site-footer{display:block}.site-footer span{display:block;margin-top:.4rem}}
/* Editorial archive palette: warm paper, ink, oxblood, and restrained bronze. */
:root{--ink:#292521;--muted:#6b6359;--line:#d8cfc2;--paper:#fffdf8;--wash:#f3efe7;--accent:#783232;--accent-dark:#542323;--warm:#a77c3f}
.site-header{background:#2d2925;color:#fffdf8;border-bottom-color:var(--warm)}
.brand{color:#fffdf8}.site-header nav a{color:#e6ddd0}.site-header nav a:hover{color:#fffdf8}
.document{box-shadow:0 10px 28px rgba(48,40,32,.07)}
.document-body blockquote{background:#f8f0e3;color:#494139}
.document-body pre{background:#2f2a26;color:#f5efe4}.document-body code{background:#eee8de}
.document-body th{background:#eee7dc}.lead{color:#4d453d}
.search-row input{border-color:#b8ac9c}.search-result p{color:#514940}
.theory-hero{background:#3a332d;color:#f7f2e9}
.theory-hero .eyebrow{color:#d9bb82}
.document-body .button{border-color:#a99b8a;color:#542323;background:#fffdf8}
.theory-hero .button{border-color:#d7c8b5;color:#3e3128}
.theory-hero .button.primary{border-color:#b58b4f;background:#b58b4f;color:#26211d}
.term-map>div{background:#faf6ee}.term-map dt{color:#542323}.term-map dd{color:#5f574e}
.claim-grid article{background:#fbf8f1}.claim-grid p{color:#51483f}
.content-card{background:#fffdf9}.content-card p{color:#625b52}
.archive-panel{background:#f7f3eb}.archive-panel summary{color:#3f3730}
'''


SEARCH_JS = r'''
(function(){
  const input=document.getElementById('search-input');
  const button=document.getElementById('search-button');
  const status=document.getElementById('search-status');
  const results=document.getElementById('search-results');
  if(!input||!button||!status||!results)return;
  const english=document.documentElement.lang.startsWith('en');
  const copy=english?{
    prompt:'Enter a keyword to search the full English Markdown archive.',
    found:n=>`${n} related page${n===1?'':'s'} found`,
    empty:'No matching pages found.',
    loading:n=>`Search ${n} English Markdown documents.`,
    failed:'The search index could not be loaded. Please browse the paper index directly.'
  }:{
    prompt:'输入关键词搜索全部 Markdown 文档的 HTML 页面。',
    found:n=>`找到 ${n} 个相关页面`,
    empty:'没有找到匹配内容。',
    loading:n=>`输入关键词搜索 ${n} 个 Markdown 文档的 HTML 页面。`,
    failed:'搜索索引加载失败，请直接浏览论文索引。'
  };
  let index=[];
  const normalize=s=>(s||'').toLocaleLowerCase().replace(/\s+/g,' ');
  function score(item,q){
    const query=normalize(q); if(!query)return 0;
    const fields=[normalize(item.title),normalize(item.keywords),normalize(item.description),normalize(item.source),normalize(item.content)];
    let n=0; if(fields[0].includes(query))n+=100; if(fields[1].includes(query))n+=35; if(fields[2].includes(query))n+=15; if(fields[3].includes(query))n+=10; if(fields[4].includes(query))n+=8;
    query.split(/[\s,，、。/]+/).filter(Boolean).forEach(t=>fields.forEach((f,i)=>{if(f.includes(t))n+=(i===0?18:i===4?1:3)})); return n;
  }
  function render(){
    const q=input.value.trim(); if(!q){status.textContent=copy.prompt;results.innerHTML='';return;}
    const found=index.map(item=>({item,s:score(item,q)})).filter(x=>x.s>0).sort((a,b)=>b.s-a.s).slice(0,50);
    status.textContent=copy.found(found.length);
    results.innerHTML=found.length?found.map(({item})=>`<article class="search-result"><h3><a href="${item.url}">${escapeHtml(item.title)}</a></h3><div class="result-meta">${escapeHtml(item.source)} · ${escapeHtml(item.section)}</div><p>${escapeHtml(item.description)}</p></article>`).join(''):`<p>${copy.empty}</p>`;
  }
  function escapeHtml(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  fetch('search.json').then(r=>r.json()).then(data=>{index=data;const q=new URLSearchParams(location.search).get('q');if(q){input.value=q;render()}else{status.textContent=copy.loading(index.length)}}).catch(()=>status.textContent=copy.failed);
  button.addEventListener('click',render); input.addEventListener('keydown',e=>{if(e.key==='Enter')render()});
})();
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build(args.output.resolve())
    print(f"Built static site in {args.output.resolve()}")
