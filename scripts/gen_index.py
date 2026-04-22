from __future__ import annotations

import html
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "work"
OUT = ROOT / "index.html"


def title_from_name(name: str) -> str:
    stem = name.removesuffix(".html")
    return stem.replace("-", " ").replace("_", " ").title()


def section_from_path(path: Path) -> str:
    if len(path.parts) == 1:
        return "root"
    return path.parts[0]


def collect_pages() -> list[dict[str, str]]:
    pages: list[dict[str, str]] = []
    for file_path in sorted(ROOT.rglob("*.html")):
        rel = file_path.relative_to(ROOT)
        if rel.as_posix() == "index.html":
            continue
        pages.append(
            {
                "path": rel.as_posix(),
                "name": file_path.name,
                "title": title_from_name(file_path.name),
                "section": section_from_path(rel),
            }
        )
    return pages


def build_html(pages: list[dict[str, str]]) -> str:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for page in pages:
        grouped[page["section"]].append(page)

    cards = []
    for section in sorted(grouped):
        links = "\n".join(
            f"""
            <a class="card" href="{html.escape(page['path'], quote=True)}">
              <div class="card-title">{html.escape(page['title'])}</div>
              <div class="card-path">{html.escape(page['path'])}</div>
            </a>
            """.strip()
            for page in grouped[section]
        )
        cards.append(
            f"""
            <section class="section">
              <div class="section-title">{html.escape(section)} <span>{len(grouped[section])} pages</span></div>
              <div class="grid">
                {links}
              </div>
            </section>
            """.strip()
        )

    body = "\n".join(cards) if cards else '<p class="empty">No HTML pages found in work/.</p>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Research Pages Index</title>
<style>
:root {{
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text: #e6edf3;
  --muted: #a7b0ba;
  --accent: #58a6ff;
  --font-sans: "Segoe UI Variable", "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei UI", "Microsoft YaHei", "Noto Sans CJK SC", "Source Han Sans SC", sans-serif;
  --font-mono: "Cascadia Mono", "Cascadia Code", Consolas, monospace;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: var(--font-sans);
  background: var(--bg);
  color: var(--text);
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}
.shell {{
  width: min(1180px, calc(100vw - 32px));
  margin: 0 auto;
  padding: 32px 0 48px;
}}
.hero {{
  background: linear-gradient(135deg, rgba(88,166,255,0.12), rgba(22,27,34,0.96));
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
}}
h1 {{
  margin: 0 0 8px;
  font-size: 34px;
}}
.sub {{
  color: var(--muted);
  line-height: 1.6;
}}
code {{
  font-family: var(--font-mono);
  font-size: 0.95em;
  background: rgba(88, 166, 255, 0.08);
  border: 1px solid rgba(88, 166, 255, 0.16);
  border-radius: 6px;
  padding: 0.08em 0.42em;
  color: #d2e7ff;
}}
.section {{
  margin-bottom: 24px;
}}
.section-title {{
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 12px;
  color: var(--accent);
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}}
.section-title span {{
  color: var(--muted);
  font-size: 12px;
  letter-spacing: 0;
  text-transform: none;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}}
.card {{
  display: block;
  text-decoration: none;
  color: inherit;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  transition: transform 0.15s ease, border-color 0.15s ease;
}}
.card:hover {{
  transform: translateY(-2px);
  border-color: var(--accent);
}}
.card-title {{
  font-weight: 600;
  margin-bottom: 6px;
}}
.card-path {{
  color: var(--muted);
  font-size: 12px;
  word-break: break-all;
}}
.empty {{
  color: var(--muted);
}}
</style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <h1>Research Pages Index</h1>
      <div class="sub">Static pages published from <code>work/</code>. This index is generated automatically by <code>scripts/gen_index.py</code>.</div>
    </section>
    {body}
  </div>
</body>
</html>
"""


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    pages = collect_pages()
    OUT.write_text(build_html(pages), encoding="utf-8")
    print(f"Generated {OUT} with {len(pages)} pages")


if __name__ == "__main__":
    main()
