#!/usr/bin/env python3
"""Export a Markdown file to a styled PDF via Playwright (Chromium print)."""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

try:
    from _paths import ROOT
except ImportError:
    ROOT = Path(__file__).resolve().parents[1]

NAVY = "#094D78"
BLUE = "#0069B4"
GOLD = "#C9A227"
INK = "#1A2E3D"
MUTED = "#345D76"

def _inline_html_raw(text: str) -> str:
    parts: list[str] = []
    pos = 0
    combined = re.compile(
        r"(\[([^\]]+)\]\(([^)]+)\)|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)"
    )
    for m in combined.finditer(text):
        if m.start() > pos:
            parts.append(html.escape(text[pos : m.start()]))
        chunk = m.group(0)
        if chunk.startswith("["):
            parts.append(
                f'<a href="{html.escape(m.group(3), quote=True)}">{html.escape(m.group(2))}</a>'
            )
        elif chunk.startswith("**"):
            parts.append(f"<strong>{html.escape(chunk[2:-2])}</strong>")
        elif chunk.startswith("*"):
            parts.append(f"<em>{html.escape(chunk[1:-1])}</em>")
        elif chunk.startswith("`"):
            parts.append(f"<code>{html.escape(chunk[1:-1])}</code>")
        pos = m.end()
    if pos < len(text):
        parts.append(html.escape(text[pos:]))
    return "".join(parts)


def parse_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def is_table_separator(line: str) -> bool:
    s = line.strip().replace("|", "").replace(":", "").replace("-", "").strip()
    return not s


def markdown_to_html(md_text: str, title: str) -> str:
    lines = md_text.splitlines()
    body: list[str] = []
    i = 0
    table_buffer: list[list[str]] = []
    in_code = False
    code_lines: list[str] = []
    skip_first_h1 = True

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                body.append(
                    "<pre><code>"
                    + html.escape("\n".join(code_lines))
                    + "</code></pre>"
                )
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            if table_buffer and is_table_separator(stripped):
                i += 1
                continue
            row = parse_table_row(stripped)
            if row:
                table_buffer.append(row)
            i += 1
            continue
        if table_buffer:
            body.append(_table_html(table_buffer))
            table_buffer = []

        if stripped == "---":
            body.append("<hr/>")
            i += 1
            continue

        for level, tag in [(4, "h4"), (3, "h3"), (2, "h2"), (1, "h1")]:
            prefix = "#" * level + " "
            if stripped.startswith(prefix):
                text = stripped[len(prefix) :].strip()
                if tag == "h1" and skip_first_h1:
                    skip_first_h1 = False
                else:
                    body.append(f"<{tag}>{_inline_html_raw(text)}</{tag}>")
                i += 1
                break
        else:
            if stripped.startswith(">"):
                quote = stripped.lstrip(">").strip()
                i += 1
                while i < len(lines) and lines[i].strip().startswith(">"):
                    quote += " " + lines[i].strip().lstrip(">").strip()
                    i += 1
                body.append(f"<blockquote><p>{_inline_html_raw(quote)}</p></blockquote>")
                continue

            bullet = re.match(r"^(\s*)[-*+]\s+(.+)$", line)
            if bullet:
                indent = len(bullet.group(1))
                tag = "ul" if indent < 2 else 'ul class="nested"'
                # collect consecutive bullets at same level - simplified single item
                body.append(
                    f"<{tag}><li>{_inline_html_raw(bullet.group(2).strip())}</li></{tag.split()[0]}>"
                )
                i += 1
                continue

            num = re.match(r"^\d+\.\s+(.+)$", stripped)
            if num:
                body.append(f"<ol><li>{_inline_html_raw(num.group(1))}</li></ol>")
                i += 1
                continue

            if not stripped:
                i += 1
                continue

            if stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("**"):
                body.append(f"<p class=\"muted\"><em>{_inline_html_raw(stripped.strip('*'))}</em></p>")
                i += 1
                continue

            body.append(f"<p>{_inline_html_raw(stripped)}</p>")
            i += 1
            continue
        continue

    if table_buffer:
        body.append(_table_html(table_buffer))

    css = f"""
    @page {{ size: A4; margin: 2cm 2.2cm 2.4cm 2.2cm; }}
    body {{
      font-family: Calibri, "Segoe UI", Arial, sans-serif;
      font-size: 11pt;
      line-height: 1.35;
      color: {INK};
    }}
    h1 {{ color: {NAVY}; font-size: 18pt; margin: 1.2em 0 0.5em; page-break-after: avoid; }}
    h2 {{ color: {BLUE}; font-size: 14pt; margin: 1em 0 0.45em; page-break-after: avoid; }}
    h3 {{ color: {NAVY}; font-size: 12pt; margin: 0.85em 0 0.35em; }}
    h4 {{ color: {BLUE}; font-size: 11pt; margin: 0.75em 0 0.3em; }}
    p {{ margin: 0 0 0.45em; text-align: justify; }}
    a {{ color: {BLUE}; }}
    code {{ font-family: Consolas, monospace; font-size: 9.5pt; background: #f4f7fa; padding: 0.1em 0.25em; }}
    pre {{
      background: #f4f7fa;
      border: 1px solid #d8edf8;
      padding: 0.6em 0.8em;
      font-size: 9pt;
      overflow-x: auto;
      white-space: pre-wrap;
    }}
    blockquote {{
      margin: 0.6em 0;
      padding: 0.5em 1em;
      border-left: 4px solid {GOLD};
      background: #eef8ff;
      color: {MUTED};
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 0.6em 0 1em;
      font-size: 10pt;
    }}
    th {{
      background: {NAVY};
      color: #fff;
      text-align: left;
      padding: 0.35em 0.5em;
    }}
    td {{
      border: 1px solid #d8edf8;
      padding: 0.3em 0.5em;
      vertical-align: top;
    }}
    tr:nth-child(even) td {{ background: #f3f9fd; }}
    ul, ol {{ margin: 0.2em 0 0.6em 1.2em; padding: 0; }}
    ul.nested {{ margin-left: 1.8em; }}
    li {{ margin: 0.15em 0; }}
    hr {{ border: none; border-top: 1px solid #d8edf8; margin: 1.2em 0; }}
    .cover {{
      text-align: center;
      padding: 3cm 0 2cm;
      page-break-after: always;
    }}
    .cover .org {{ font-size: 11pt; color: {MUTED}; letter-spacing: 0.06em; text-transform: uppercase; }}
    .cover h1 {{ font-size: 22pt; border: none; margin-top: 1.5em; }}
    .cover .rule {{ color: {GOLD}; margin: 0.8em 0; }}
    .cover .meta {{ font-size: 10pt; color: {MUTED}; margin-top: 2em; }}
    """

    cover_title = title
    for ln in md_text.splitlines():
        if ln.strip().startswith("# "):
            cover_title = ln.strip()[2:].strip()
            break

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{html.escape(cover_title)}</title>
<style>{css}</style>
</head>
<body>
<div class="cover">
  <p class="org">World Association of Azerbaijani Scientists<br/>Dünya Azərbaycanlı Alimlər Birliyi (WAAS / DAAB)</p>
  <h1>{html.escape(cover_title)}</h1>
  <p class="rule">━━━━━━━━━━━━━━━━━━━━━━━━</p>
  <p class="meta">User manual · PDF export</p>
</div>
{"".join(body)}
</body>
</html>"""


def _table_html(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    parts = ["<table><thead><tr>"]
    for cell in rows[0]:
        parts.append(f"<th>{_inline_html_raw(cell)}</th>")
    parts.append("</tr></thead><tbody>")
    for row in rows[1:]:
        parts.append("<tr>")
        for cell in row:
            parts.append(f"<td>{_inline_html_raw(cell)}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def export_markdown_to_pdf(md_path: Path, pdf_path: Path) -> Path:
    md_text = md_path.read_text(encoding="utf-8")
    html_doc = markdown_to_html(md_text, md_path.stem)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html_doc, wait_until="networkidle")
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "20mm", "bottom": "22mm", "left": "22mm", "right": "22mm"},
        )
        browser.close()
    return pdf_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Markdown to styled PDF")
    parser.add_argument("markdown", nargs="?", help="Path to .md file")
    parser.add_argument("-o", "--output", help="Output .pdf path")
    args = parser.parse_args()

    md_path = Path(args.markdown) if args.markdown else ROOT / "documents/DAAB-Website-User-Manual.md"
    if not md_path.is_file():
        print(f"Not found: {md_path}", file=sys.stderr)
        return 1

    pdf_path = Path(args.output) if args.output else ROOT / "documents/pdf" / (md_path.stem + ".pdf")
    export_markdown_to_pdf(md_path, pdf_path)
    print(pdf_path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
