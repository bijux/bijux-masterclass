#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

CSS = """
:root {
  --bg: #0b0f14;
  --fg: #e6edf3;
  --muted: #9da7b3;
  --card: #111826;
  --border: #263142;
  --accent: #6ea8fe;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg: #ffffff;
    --fg: #111827;
    --muted: #4b5563;
    --card: #f8fafc;
    --border: #e5e7eb;
    --accent: #2563eb;
  }
}
body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial,
    "Apple Color Emoji", "Segoe UI Emoji";
  background: var(--bg);
  color: var(--fg);
}
header { padding: 28px 22px; border-bottom: 1px solid var(--border); }
h1 { margin: 0 0 6px 0; font-size: 22px; }
p { margin: 8px 0; color: var(--muted); line-height: 1.5; }
main { max-width: 1100px; margin: 0 auto; padding: 22px; }
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  margin: 14px 0;
}
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
@media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td { border-bottom: 1px solid var(--border); padding: 8px 10px; text-align: left; }
th { color: var(--muted); font-weight: 600; }
small { color: var(--muted); }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
svg { width: 100%; height: auto; }
"""


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def svg_polyline(y: list[float], *, height: int = 160, pad: int = 12) -> str:
    if not y:
        return "<svg viewBox='0 0 400 160'></svg>"
    w = 400
    h = height
    xmin = 0
    xmax = max(1, len(y) - 1)
    ymin = min(y)
    ymax = max(y)
    if ymax == ymin:
        ymax = ymin + 1.0

    def x(i: int) -> float:
        return pad + (w - 2 * pad) * (i - xmin) / (xmax - xmin)

    def yy(v: float) -> float:
        return (h - pad) - (h - 2 * pad) * (v - ymin) / (ymax - ymin)

    pts = " ".join(f"{x(i):.2f},{yy(v):.2f}" for i, v in enumerate(y))
    label = f"Q {ymin:.1f}–{ymax:.1f}"
    return (
        f"<svg viewBox='0 0 {w} {h}' role='img' aria-label='quality plot'>"
        f"<polyline fill='none' stroke='currentColor' stroke-width='2' points='{pts}'/>"
        f"<text x='{pad}' y='{pad + 10}' font-size='10' fill='currentColor'>"
        f"{label}"
        f"</text>"
        f"</svg>"
    )


def svg_hist(hist: dict[str, int], *, height: int = 160, pad: int = 12) -> str:
    if not hist:
        return "<svg viewBox='0 0 400 160'></svg>"
    w = 400
    h = height
    xs = sorted((int(k), int(v)) for k, v in hist.items())
    counts = [v for _, v in xs]
    ymax = max(counts) if counts else 1

    n = len(xs)
    bar_w = (w - 2 * pad) / max(1, n)

    parts = [f"<svg viewBox='0 0 {w} {h}' role='img' aria-label='length histogram'>"]
    for i, (_L, c) in enumerate(xs):
        x = pad + i * bar_w
        bh = (h - 2 * pad) * (c / ymax) if ymax else 0
        y = (h - pad) - bh
        rect = (
            f"<rect x='{x:.2f}' y='{y:.2f}' width='{bar_w * 0.92:.2f}' "
            f"height='{bh:.2f}' fill='currentColor' opacity='0.35'/>"
        )
        parts.append(rect)
    parts.append(
        f"<text x='{pad}' y='{pad + 10}' font-size='10' fill='currentColor'>max count {ymax}</text>"
    )
    parts.append("</svg>")
    return "".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary-json", required=True)
    ap.add_argument("--out-html", required=True)
    args = ap.parse_args()

    summary = json.loads(Path(args.summary_json).read_text(encoding="utf-8"))
    out_html = Path(args.out_html)
    out_html.parent.mkdir(parents=True, exist_ok=True)

    units = summary.get("units", {})

    # Build overview table
    rows = []
    for name, d in units.items():
        h = d["highlights"]
        top = d["screen"]["top_hit"]
        rows.append(
            "<tr>"
            f"<td><b>{esc(name)}</b></td>"
            f"<td>{h['reads_raw']}</td>"
            f"<td>{h['reads_trimmed']}</td>"
            f"<td>{h['reads_dedup']}</td>"
            f"<td>{float(d['raw_qc']['gc_fraction']):.3f}</td>"
            f"<td>{float(h['mean_q_raw']):.1f}</td>"
            f"<td>{float(h['mean_q_trimmed']):.1f}</td>"
            f"<td>{esc(top.get('panel'))}</td>"
            f"<td>{float(top.get('signature_overlap', 0.0)):.3f}</td>"
            "</tr>"
        )

    overview_table = (
        "<table>"
        "<thead><tr>"
        "<th>sample</th><th>reads (raw)</th><th>reads (trim)</th><th>reads (dedup)</th>"
        "<th>GC (raw)</th><th>mean Q (raw)</th><th>mean Q (trim)</th>"
        "<th>top panel</th><th>score</th>"
        "</tr></thead>"
        "<tbody>" + "".join(rows) + "</tbody></table>"
    )

    # Per-sample cards
    cards = []
    for name, d in units.items():
        raw = d["raw_qc"]
        trm = d["trimmed_qc"]
        raw_plot = svg_polyline(list(map(float, raw["qual_mean_per_pos"])))
        trm_plot = svg_polyline(list(map(float, trm["qual_mean_per_pos"])))
        raw_hist = svg_hist(raw.get("length_hist", {}))
        trm_hist = svg_hist(trm.get("length_hist", {}))

        stats_line = (
            f"raw: {raw['reads']} reads, {raw['bases']} bases · "
            f"trimmed: {trm['reads']} reads, {trm['bases']} bases · "
            f"unique kmers: {d['kmer']['unique_kmers']}"
        )

        cards.append(
            "<section class='card'>"
            f"<h2 style='margin:0 0 6px 0;font-size:18px'>{esc(name)}</h2>"
            f"<p><small>{stats_line}</small></p>"
            "<div class='grid'>"
            "<div class='card'>"
            "<h3 style='margin:0 0 6px 0;font-size:14px;color:var(--muted)'>Quality (raw)</h3>"
            f"{raw_plot}"
            "<h3 style='margin:10px 0 6px 0;font-size:14px;color:var(--muted)'>"
            "Read length (raw)"
            "</h3>"
            f"{raw_hist}"
            "</div>"
            "<div class='card'>"
            "<h3 style='margin:0 0 6px 0;font-size:14px;color:var(--muted)'>Quality (trimmed)</h3>"
            f"{trm_plot}"
            "<h3 style='margin:10px 0 6px 0;font-size:14px;color:var(--muted)'>"
            "Read length (trimmed)"
            "</h3>"
            f"{trm_hist}"
            "</div>"
            "</div>"
            "</section>"
        )

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Deep Dive Snakemake — Capstone Report</title>
  <style>{CSS}</style>
</head>
<body>
<header>
  <h1>Capstone report</h1>
  <p>
    Python-first FASTQ QC + trimming + dedup + k-mer screening (Snakemake).
    Deterministic outputs, no conda, no external binaries.
  </p>
</header>
<main>
  <div class="card">
    <h2 style="margin:0 0 10px 0;font-size:16px">Overview</h2>
    {overview_table}
  </div>
  {"".join(cards)}
</main>
</body>
</html>
"""
    out_html.write_text(html_doc, encoding="utf-8")


if __name__ == "__main__":
    main()
