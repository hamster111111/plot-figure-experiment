from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "work"
OUT = ROOT / "index.html"

PAGE_META: dict[str, dict[str, object]] = {
    "research-overview.html": {
        "title": "Research Overview",
        "layer": "layer0",
        "order": 10,
        "note": "总入口页，串起当前方向判断、关键结论和各专题入口。",
    },
    "research-summary.html": {
        "title": "Executive Summary",
        "layer": "layer0",
        "order": 20,
        "note": "给师兄/自己快速过一遍当前结论、风险和下一步判断。",
    },
    "research-timeline.html": {
        "title": "Timeline & Risks",
        "layer": "layer0",
        "order": 30,
        "note": "按时间线记录推进过程，并把风险项单独拎出来看。",
    },
    "research-thesis.html": {
        "title": "Thesis Framing",
        "layer": "layer1",
        "order": 10,
        "note": "集中论证 F-A 现在应该怎么 framing，适合往论文主线收敛。",
    },
    "research-selection.html": {
        "title": "Benchmark Selection",
        "layer": "layer1",
        "order": 20,
        "note": "讨论 bench 该怎么选、主实验放哪、哪些只配做补充。",
    },
    "research-benchmarks.html": {
        "title": "Benchmark Overview",
        "layer": "layer1",
        "order": 30,
        "note": "把 MatPlotBench / Text2Vis / VisEval 等复现结果放在一页总览里。",
    },
    "research-competitors.html": {
        "title": "Competitor Panorama",
        "layer": "layer1",
        "order": 40,
        "note": "看竞品和我们是不是正交、谁是真威胁、谁只是 related work。",
    },
    "competitive-intel.html": {
        "title": "Competitive Intel",
        "layer": "layer1",
        "order": 50,
        "note": "最细的调研与复现笔记，信息最杂但证据最全。",
    },
    "plotting-authority.html": {
        "title": "Authority Landscape",
        "layer": "layer1",
        "order": 60,
        "note": "按权威度筛 plotting 相关 bench 和 framework，帮助判断主叙事放哪。",
    },
    "plotting-benchmarks.html": {
        "title": "Plotting Benchmark Catalog",
        "layer": "layer1",
        "order": 70,
        "note": "更像卡片库，适合扫有哪些 plotting bench、各自测什么。",
    },
    "research-bench-text2vis.html": {
        "title": "Text2Vis Cases",
        "layer": "layer2",
        "order": 10,
        "note": "Text2Vis 失败样例页，专门看答案错、计算错、格式错这些问题。",
    },
    "research-bench-viseval.html": {
        "title": "VisEval Cases",
        "layer": "layer2",
        "order": 20,
        "note": "VisEval 失败样例页，重点看 groupby / filter / data_check 这类错误。",
    },
    "research-bench-matplot.html": {
        "title": "MatPlotBench Cases",
        "layer": "layer2",
        "order": 30,
        "note": "MatPlotBench 典型好坏例子，主要观察图像质量和结构偏差。",
    },
    "research-failure.html": {
        "title": "Failure Analysis",
        "layer": "layer2",
        "order": 40,
        "note": "把失败模式再抽象一层，帮助从 case 走向框架问题。",
    },
}

LAYER_META: list[dict[str, str]] = [
    {
        "key": "layer0",
        "title": "Layer 0",
        "subtitle": "总览层",
        "desc": "先看整体判断和导航。",
    },
    {
        "key": "layer1",
        "title": "Layer 1",
        "subtitle": "策略层",
        "desc": "再看 framing、选型、竞品和 landscape。",
    },
    {
        "key": "layer2",
        "title": "Layer 2",
        "subtitle": "证据层",
        "desc": "最后下钻到具体 bench case 和失败证据。",
    },
]


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
        meta = PAGE_META.get(rel.as_posix(), {})
        pages.append(
            {
                "path": rel.as_posix(),
                "name": file_path.name,
                "title": str(meta.get("title", title_from_name(file_path.name))),
                "section": section_from_path(rel),
                "layer": str(meta.get("layer", "layer2")),
                "note": str(meta.get("note", "Static page.")),
                "order": int(meta.get("order", 999)),
            }
        )
    return sorted(pages, key=lambda page: (page["layer"], page["order"], page["path"]))


def build_html(pages: list[dict[str, str]]) -> str:
    grouped: dict[str, list[dict[str, str]]] = {item["key"]: [] for item in LAYER_META}
    for page in pages:
        grouped.setdefault(page["layer"], []).append(page)

    columns = []
    for layer in LAYER_META:
        items = grouped.get(layer["key"], [])
        cards = "\n".join(
            f"""
            <a class="card" href="{html.escape(page['path'], quote=True)}">
              <div class="card-title">{html.escape(page['title'])}</div>
              <div class="card-note">{html.escape(page['note'])}</div>
              <div class="card-path">{html.escape(page['path'])}</div>
            </a>
            """.strip()
            for page in items
        )
        columns.append(
            f"""
            <section class="lane">
              <div class="lane-head">
                <div class="lane-kicker">{html.escape(layer['title'])}</div>
                <div class="lane-title">{html.escape(layer['subtitle'])}</div>
                <div class="lane-desc">{html.escape(layer['desc'])}</div>
                <div class="lane-count">{len(items)} pages</div>
              </div>
              <div class="lane-stack">
                {cards or '<p class="empty">No pages.</p>'}
              </div>
            </section>
            """.strip()
        )

    body = f'<div class="board">{"".join(columns)}</div>' if columns else '<p class="empty">No HTML pages found in work/.</p>'
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
.board {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  align-items: start;
}}
.lane {{
  min-width: 0;
}}
.lane-head {{
  background: linear-gradient(180deg, rgba(88,166,255,0.1), rgba(22,27,34,0.92));
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 16px;
  margin-bottom: 14px;
}}
.lane-kicker {{
  color: var(--accent);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 6px;
}}
.lane-title {{
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 6px;
}}
.lane-desc {{
  color: var(--muted);
  line-height: 1.6;
  font-size: 14px;
}}
.lane-count {{
  margin-top: 10px;
  color: var(--muted);
  font-size: 12px;
}}
.lane-stack {{
  display: grid;
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
.card-note {{
  color: var(--text);
  opacity: 0.92;
  line-height: 1.55;
  margin-bottom: 10px;
  font-size: 14px;
}}
.card-path {{
  color: var(--muted);
  font-size: 12px;
  word-break: break-all;
}}
.empty {{
  color: var(--muted);
}}
@media (max-width: 980px) {{
  .board {{
    grid-template-columns: 1fr;
  }}
}}
</style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <h1>Research Pages Index</h1>
      <div class="sub">Static pages published from <code>work/</code>. This index is generated automatically by <code>scripts/gen_index.py</code>. Pages are grouped by reading hierarchy so you can go from overview to strategy to evidence.</div>
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
