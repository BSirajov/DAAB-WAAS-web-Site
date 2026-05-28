#!/usr/bin/env python3
"""Repair forum CSS selector lists where a page id line is missing the descendant suffix."""
import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "css" / "daab-forum-content.css"
text = p.read_text(encoding="utf-8")

# photos-gallery"],\n...video-gallery"]<suffix>{
text = re.sub(
    r'html\[data-daab-page-id="forum-photos-gallery"\],\s*\n'
    r'html\[data-daab-page-id="forum-video-gallery"\]([^\{]*)\{',
    r'html[data-daab-page-id="forum-photos-gallery"]\1,\n'
    r'html[data-daab-page-id="forum-video-gallery"]\1{',
    text,
    flags=re.S,
)

# bagli-hekayeler"],\n...cooperation"]<suffix>{
text = re.sub(
    r'html\[data-daab-page-id="forum-bagli-hekayeler"\],\s*\n'
    r'html\[data-daab-page-id="forum-cooperation"\]([^\{]*)\{',
    r'html[data-daab-page-id="forum-bagli-hekayeler"]\1,\n'
    r'html[data-daab-page-id="forum-cooperation"]\1{',
    text,
    flags=re.S,
)

# Remove duplicated widget-head/card-header gradient block (lines ~265–287 corruption)
old_mess = """html[data-daab-page-id="forum-official"] .card-header,
html[data-daab-page-id="forum-2024-presentations"] .card-header,
html[data-daab-page-id="forum-program"] .card-header,
html[data-daab-page-id="forum-impressions"] .card-header,
html[data-daab-page-id="forum-roadmap"] .card-header,
html[data-daab-page-id="forum-official"] .widget-head,
html[data-daab-page-id="forum-2024-presentations"] .widget-head,
html[data-daab-page-id="forum-program"] .widget-head,
html[data-daab-page-id="forum-impressions"] .widget-head,
html[data-daab-page-id="forum-roadmap"] .widget-head,
html[data-daab-page-id="forum-bagli-hekayeler"] .widget-head,
html[data-daab-page-id="forum-cooperation"] .widget-head,
html[data-daab-page-id="forum-bagli-hekayeler"] .card-header,
html[data-daab-page-id="forum-cooperation"] .card-header,
html[data-daab-page-id="forum-official"] .widget-head,
html[data-daab-page-id="forum-2024-presentations"] .widget-head,
html[data-daab-page-id="forum-program"] .widget-head,
html[data-daab-page-id="forum-impressions"] .widget-head,
html[data-daab-page-id="forum-roadmap"] .widget-head,
html[data-daab-page-id="forum-bagli-hekayeler"] .widget-head,
html[data-daab-page-id="forum-cooperation"] .widget-head{"""

new_block = """html[data-daab-page-id="forum-official"] .card-header,
html[data-daab-page-id="forum-2024-presentations"] .card-header,
html[data-daab-page-id="forum-program"] .card-header,
html[data-daab-page-id="forum-impressions"] .card-header,
html[data-daab-page-id="forum-roadmap"] .card-header,
html[data-daab-page-id="forum-bagli-hekayeler"] .card-header,
html[data-daab-page-id="forum-cooperation"] .card-header,
html[data-daab-page-id="forum-official"] .widget-head,
html[data-daab-page-id="forum-2024-presentations"] .widget-head,
html[data-daab-page-id="forum-program"] .widget-head,
html[data-daab-page-id="forum-impressions"] .widget-head,
html[data-daab-page-id="forum-roadmap"] .widget-head,
html[data-daab-page-id="forum-bagli-hekayeler"] .widget-head,
html[data-daab-page-id="forum-cooperation"] .widget-head{"""

if old_mess not in text:
    # try post-regex state
    old_mess2 = old_mess.replace(
        'html[data-daab-page-id="forum-bagli-hekayeler"] .widget-head,\n'
        'html[data-daab-page-id="forum-cooperation"] .widget-head,\n'
        'html[data-daab-page-id="forum-bagli-hekayeler"] .card-header,\n'
        'html[data-daab-page-id="forum-cooperation"] .card-header,\n'
        'html[data-daab-page-id="forum-official"] .widget-head,',
        'html[data-daab-page-id="forum-bagli-hekayeler"],\n'
        'html[data-daab-page-id="forum-cooperation"] .widget-head,\n'
        'html[data-daab-page-id="forum-bagli-hekayeler"],\n'
        'html[data-daab-page-id="forum-cooperation"] .card-header,\n'
        'html[data-daab-page-id="forum-official"] .widget-head,',
    )
    if old_mess2 in text:
        text = text.replace(old_mess2, new_block)
else:
    text = text.replace(old_mess, new_block)

# Dedupe scroll-behavior block for stories/cooperation
scroll_dup = """html[data-daab-page-id="forum-roadmap"] .timeline-list a,
html[data-daab-page-id="forum-bagli-hekayeler"] .timeline-list a ,
html[data-daab-page-id="forum-cooperation"] .timeline-list a ,
html[data-daab-page-id="forum-bagli-hekayeler"],
html[data-daab-page-id="forum-cooperation"] {
  scroll-behavior: auto !important;
}

html[data-daab-page-id="forum-official"] .timeline-list a,
html[data-daab-page-id="forum-program"] .timeline-list a,
html[data-daab-page-id="forum-2024-presentations"] .timeline-list a,
html[data-daab-page-id="forum-impressions"] .timeline-list a,
html[data-daab-page-id="forum-roadmap"] .timeline-list a,
html[data-daab-page-id="forum-bagli-hekayeler"],
html[data-daab-page-id="forum-cooperation"] .timeline-list a {"""

scroll_fix = """html[data-daab-page-id="forum-roadmap"] .timeline-list a,
html[data-daab-page-id="forum-bagli-hekayeler"] .timeline-list a,
html[data-daab-page-id="forum-cooperation"] .timeline-list a,
html[data-daab-page-id="forum-bagli-hekayeler"],
html[data-daab-page-id="forum-cooperation"] {
  scroll-behavior: auto !important;
}

html[data-daab-page-id="forum-official"] .timeline-list a,
html[data-daab-page-id="forum-program"] .timeline-list a,
html[data-daab-page-id="forum-2024-presentations"] .timeline-list a,
html[data-daab-page-id="forum-impressions"] .timeline-list a,
html[data-daab-page-id="forum-roadmap"] .timeline-list a,
html[data-daab-page-id="forum-bagli-hekayeler"] .timeline-list a,
html[data-daab-page-id="forum-cooperation"] .timeline-list a {"""

if scroll_dup in text:
    text = text.replace(scroll_dup, scroll_fix)

p.write_text(text, encoding="utf-8")
print("fixed css pairs")
