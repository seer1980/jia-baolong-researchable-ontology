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
    return "https://YOUR-USERNAME.github.io/YOUR-REPOSITORY"


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
        if not path_part.endswith(".md"):
            return match.group(0)
        candidate = (source.parent / path_part).resolve()
        try:
            relative_source = candidate.relative_to(ROOT)
        except ValueError:
            return match.group(0)
        if not candidate.exists():
            return match.group(0)
        destination = output_path(ROOT / relative_source)
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
) -> str:
    meta = meta or {}
    home = relative_url(target, Path("index.html"))
    search = relative_url(target, Path("search.html"))
    papers = relative_url(target, Path("papers/index.html"))
    guides = relative_url(target, Path("guide/index.html"))
    styles = relative_url(target, Path("assets/styles.css"))
    script = relative_url(target, Path("assets/search.js"))
    canonical_path = "" if target == Path("index.html") else f"/{target.as_posix()}"
    canonical = f"{base_url}{canonical_path}"
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
    visible_title = render_title(display_title or title)
    if section == "paper":
        json_ld["author"] = {"@type": "Person", "name": author}
        if date:
            json_ld["datePublished"] = date
        if meta.get("doi"):
            json_ld["sameAs"] = f"https://doi.org/{meta['doi']}"
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · Jia Baolong Absolute Truth Theory</title>
  <meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="canonical" href="{html.escape(canonical, quote=True)}">
  <link rel="stylesheet" href="{styles}">
  <script>window.MathJax = {{tex: {{inlineMath: [['\\\\(', '\\\\)'], ['$', '$']], displayMath: [['\\\\[', '\\\\]'], ['$$', '$$']]}}, options: {{skipHtmlTags: ['script','noscript','style','textarea','pre','code']}}}};</script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <script defer src="{script}"></script>
  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="{home}">贾宝龙绝对真理理论</a>
      <nav aria-label="主导航"><a href="{home}">首页</a><a href="{guides}">理论导读</a><a href="{papers}">论文</a><a href="{search}">搜索</a></nav>
    </div>
  </header>
  <main class="page-shell">
    <div class="breadcrumbs"><a href="{home}">首页</a> <span>›</span> <span>{html.escape(section)}</span></div>
    <article class="document">
      <h1>{visible_title}</h1>
      {meta_html}
      <div class="document-body">{body_html}</div>
    </article>
  </main>
  <footer class="site-footer"><a href="{home}">贾宝龙绝对真理理论</a><span>Markdown 全文 · HTML 网站</span></footer>
</body>
</html>
'''


def render_markdown(body: str) -> str:
    protected, replacements = protect_math(body)
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


def build(output_root: Path) -> None:
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    base_url = default_base_url()
    repo_url = repository_url()
    entries: list[dict[str, Any]] = []
    source_files = sorted(
        p
        for p in ROOT.rglob("*.md")
        if "site" not in p.relative_to(ROOT).parts
        and ".git" not in p.relative_to(ROOT).parts
        and "tools" not in p.relative_to(ROOT).parts
    )
    for source in source_files:
        relative = source.relative_to(ROOT)
        text = source.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        title = meta.get("title") or first_heading(body)
        if relative.as_posix() == "README.md":
            title = "贾宝龙绝对真理理论：论文与研究档案"
        display_title = title if relative.as_posix() == "README.md" else first_heading(body)
        description = shorten(body, 260)
        section = "paper" if relative.parts[0] in {"papers", "supplementary_transcriptions"} else "guide"
        target = output_path(source)
        rendered = strip_first_h1(rewrite_markdown_links(render_markdown(body), source, target))
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
        )
        write_page(output_root, target, content)
        entries.append(
            {
                "title": title,
                "description": description,
                "source": relative.as_posix(),
                "url": target.as_posix(),
                "section": section,
                "author": meta.get("author", "Jia Baolong"),
                "date": meta.get("publication_date", ""),
                "zenodo_url": meta.get("zenodo_url", ""),
                "doi": meta.get("doi", ""),
                "keywords": " ".join(
                    filter(None, [title, meta.get("author", ""), meta.get("document_role", ""), relative.stem])
                ),
            }
        )

    papers = [entry for entry in entries if entry["section"] == "paper"]
    guides = [entry for entry in entries if entry["section"] == "guide"]
    paper_items = "".join(
        f'<li><a href="{html.escape(relative_url(Path("papers/index.html"), Path(entry["url"])), quote=True)}">{html.escape(entry["title"])}</a><span>{html.escape(entry["source"])}</span></li>'
        for entry in papers
    )
    guide_items = "".join(
        f'<li><a href="{html.escape(relative_url(Path("guide/index.html"), Path(entry["url"])), quote=True)}">{html.escape(entry["title"])}</a><span>{html.escape(entry["source"])}</span></li>'
        for entry in guides
    )
    papers_body = f'''<p class="lead">本页列出 32 篇论文正文和 7 篇 PDF 全文恢复，均可直接搜索、阅读和引用。</p>
<h2>论文与 PDF 全文</h2><ul class="directory-list">{paper_items}</ul>'''
    guides_body = f'''<p class="lead">理论导读、完整阅读指南、术语、第一拍论证和涌现链。</p>
<ul class="directory-list">{guide_items}</ul>'''
    write_page(
        output_root,
        Path("papers/index.html"),
        page_template(
            title="论文全文索引",
            description="贾宝龙理论论文正文与 PDF 全文恢复索引。",
            body_html=papers_body,
            target=Path("papers/index.html"),
            base_url=base_url,
            section="papers",
        ),
    )
    write_page(
        output_root,
        Path("guide/index.html"),
        page_template(
            title="理论导读索引",
            description="贾宝龙绝对真理理论的完整阅读入口、理论结构和公式导读。",
            body_html=guides_body,
            target=Path("guide/index.html"),
            base_url=base_url,
            section="guide",
        ),
    )
    write_page(
        output_root,
        Path("search.html"),
        page_template(
            title="全文搜索",
            description="搜索贾宝龙绝对真理理论的论文、公式和理论导读。",
            body_html='''<section class="search-panel"><label for="search-input">搜索论文、公式和理论概念</label><div class="search-row"><input id="search-input" type="search" placeholder="例如：PR、Undefined、第一拍、类物质、Rule 979" autocomplete="off"><button id="search-button" type="button">搜索</button></div><p id="search-status" class="search-status">正在加载全文索引…</p><div id="search-results" class="search-results" aria-live="polite"></div></section>''',
            target=Path("search.html"),
            base_url=base_url,
            section="search",
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

    assets = output_root / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "styles.css").write_text(STYLES_CSS, encoding="utf-8")
    (assets / "search.js").write_text(SEARCH_JS, encoding="utf-8")
    (output_root / "search.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_root / ".nojekyll").write_text("", encoding="utf-8")
    sitemap_urls = [f"{base_url}/" if entry["url"] == "index.html" else f"{base_url}/{entry['url']}" for entry in entries]
    sitemap_urls.extend([f"{base_url}/papers/", f"{base_url}/guide/", f"{base_url}/search.html"])
    sitemap = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
    sitemap += "".join(f"  <url><loc>{html.escape(url)}</loc></url>\n" for url in sorted(set(sitemap_urls)))
    sitemap += "</urlset>\n"
    (output_root / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (output_root / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {base_url}/sitemap.xml\n",
        encoding="utf-8",
    )
    (output_root / "site-config.json").write_text(
        json.dumps({"base_url": base_url, "github_repository": repo_url, "source_markdown_count": len(source_files)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


STYLES_CSS = r'''
:root{--ink:#132238;--muted:#5c6b7c;--line:#dbe3ec;--paper:#ffffff;--wash:#f4f7fb;--accent:#1264a3;--accent-dark:#0b4778;--warm:#f0b44d;}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--wash);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.72}.site-header{background:#0e2238;color:#fff;border-bottom:4px solid var(--warm)}.header-inner{max-width:1180px;margin:auto;padding:1rem 1.25rem;display:flex;align-items:center;justify-content:space-between;gap:1.5rem}.brand{color:#fff;text-decoration:none;font-weight:760;letter-spacing:.02em}.site-header nav{display:flex;gap:1rem;flex-wrap:wrap}.site-header nav a{color:#d8e9f7;text-decoration:none;font-size:.92rem}.site-header nav a:hover{color:#fff}.page-shell{max-width:1040px;margin:0 auto;padding:1.25rem 1.1rem 4rem}.breadcrumbs{color:var(--muted);font-size:.88rem;margin:.25rem 0 1rem}.breadcrumbs a{color:var(--accent)}.document{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:clamp(1.2rem,3vw,3rem);box-shadow:0 12px 38px rgba(22,47,76,.07)}h1,h2,h3,h4{line-height:1.24;color:var(--ink)}h1{font-size:clamp(1.9rem,4.5vw,3.1rem);margin:.1rem 0 .6rem}h2{margin-top:2.3rem;border-bottom:1px solid var(--line);padding-bottom:.35rem}h3{margin-top:1.6rem}.page-meta{display:flex;flex-wrap:wrap;gap:.35rem .8rem;color:var(--muted);font-size:.9rem;padding:.55rem 0 1.35rem;border-bottom:1px solid var(--line)}.page-meta a{color:var(--accent)}.document-body{font-size:1.02rem}.document-body a{color:var(--accent-dark)}.document-body img{max-width:100%;height:auto}.document-body blockquote{border-left:4px solid var(--warm);background:#fff8e9;margin:1.2rem 0;padding:.65rem 1rem;color:#37465a}.document-body pre{overflow:auto;background:#142436;color:#eaf3fb;padding:1rem;border-radius:10px}.document-body code{background:#eef3f8;padding:.12rem .3rem;border-radius:4px}.document-body pre code{background:transparent;padding:0}.document-body table{border-collapse:collapse;display:block;overflow:auto;width:100%;margin:1rem 0}.document-body th,.document-body td{border:1px solid var(--line);padding:.5rem .7rem;text-align:left;vertical-align:top}.document-body th{background:#edf4fa}.document-body .math-block{text-align:center;overflow:auto}.lead{font-size:1.12rem;color:#344963}.directory-list{list-style:none;padding:0;margin:1rem 0}.directory-list li{display:flex;justify-content:space-between;gap:1rem;border-bottom:1px solid var(--line);padding:.72rem .2rem}.directory-list li span{color:var(--muted);font-size:.88rem;text-align:right}.search-panel{max-width:800px;margin:0 auto}.search-panel label{display:block;font-weight:700;margin-bottom:.45rem}.search-row{display:flex;gap:.6rem}.search-row input{flex:1;border:1px solid #aebdcd;border-radius:8px;padding:.75rem .85rem;font:inherit}.search-row button{border:0;border-radius:8px;padding:.75rem 1.2rem;background:var(--accent);color:#fff;font:inherit;font-weight:700;cursor:pointer}.search-row button:hover{background:var(--accent-dark)}.search-status{color:var(--muted);font-size:.92rem}.search-result{border-top:1px solid var(--line);padding:1rem 0}.search-result h3{margin:0 0 .2rem}.search-result p{margin:.25rem 0;color:#41546b}.result-meta{font-size:.82rem;color:var(--muted)}.site-footer{max-width:1040px;margin:auto;padding:1.25rem 1.1rem 3rem;display:flex;justify-content:space-between;gap:1rem;color:var(--muted);font-size:.86rem}.site-footer a{color:var(--accent)}@media(max-width:680px){.header-inner{display:block}.site-header nav{margin-top:.7rem}.directory-list li{display:block}.directory-list li span{display:block;text-align:left;margin-top:.2rem}.site-footer{display:block}.site-footer span{display:block;margin-top:.4rem}}
'''


SEARCH_JS = r'''
(function(){
  const input=document.getElementById('search-input');
  const button=document.getElementById('search-button');
  const status=document.getElementById('search-status');
  const results=document.getElementById('search-results');
  if(!input||!button||!status||!results)return;
  let index=[];
  const normalize=s=>(s||'').toLocaleLowerCase().replace(/\s+/g,' ');
  function score(item,q){
    const query=normalize(q); if(!query)return 0;
    const fields=[normalize(item.title),normalize(item.keywords),normalize(item.description),normalize(item.source)];
    let n=0; if(fields[0].includes(query))n+=100; if(fields[1].includes(query))n+=35; if(fields[2].includes(query))n+=15; if(fields[3].includes(query))n+=10;
    query.split(/[\s,，、。/]+/).filter(Boolean).forEach(t=>fields.forEach((f,i)=>{if(f.includes(t))n+=(i===0?18:3)})); return n;
  }
  function render(){
    const q=input.value.trim(); if(!q){status.textContent='输入关键词搜索 53 个 Markdown 文档的 HTML 页面。';results.innerHTML='';return;}
    const found=index.map(item=>({item,s:score(item,q)})).filter(x=>x.s>0).sort((a,b)=>b.s-a.s).slice(0,50);
    status.textContent=`找到 ${found.length} 个相关页面`;
    results.innerHTML=found.length?found.map(({item})=>`<article class="search-result"><h3><a href="${item.url}">${escapeHtml(item.title)}</a></h3><div class="result-meta">${escapeHtml(item.source)} · ${escapeHtml(item.section)}</div><p>${escapeHtml(item.description)}</p></article>`).join(''):'<p>没有找到匹配内容。</p>';
  }
  function escapeHtml(s){return String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  fetch('search.json').then(r=>r.json()).then(data=>{index=data;const q=new URLSearchParams(location.search).get('q');if(q){input.value=q;render()}else{status.textContent='输入关键词搜索 53 个 Markdown 文档的 HTML 页面。'}}).catch(()=>status.textContent='搜索索引加载失败，请直接浏览论文索引。');
  button.addEventListener('click',render); input.addEventListener('keydown',e=>{if(e.key==='Enter')render()});
})();
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build(args.output.resolve())
    print(f"Built static site in {args.output.resolve()}")
