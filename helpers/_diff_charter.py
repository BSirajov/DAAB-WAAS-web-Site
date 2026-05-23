#!/usr/bin/env python3
"""One-shot: compare az/charter.html vs en/charter.html and print a structural diff."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT


def extract_structure(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    title = re.search(r"<title>([^<]*)</title>", text)
    md1 = re.findall(r'<meta[^>]+name="description"[^>]*content="([^"]*)"', text)
    md2 = re.findall(r'<meta[^>]+content="([^"]*)"[^>]+name="description"', text)
    meta_descs = md1 + md2
    og_title = re.findall(r'property="og:title"[^>]*content="([^"]*)"', text)
    og_desc = re.findall(r'property="og:description"[^>]*content="([^"]*)"', text)
    html_attrs = re.search(r"<html([^>]*)>", text)

    css_links = re.findall(r'<link[^>]+href="([^"]+\.css[^"]*)"', text)
    scripts = re.findall(r'<script[^>]*src="([^"]+\.js[^"]*)"', text)

    widget_title = re.search(
        r'<div class="widget-head">.*?<h3[^>]*>([^<]+)</h3>', text, re.DOTALL
    )
    toc_items = re.findall(
        r'<li><span class="tl-date">([^<]+)</span><a href="(#section-\d+)">([^<]+)</a></li>',
        text,
    )

    sections = re.findall(
        r'<section class="charter-card" id="(section-\d+)">\s*'
        r'<div class="article-separate-title">([^<]*(?:<br/>[^<]*)*)</div>\s*'
        r'<div class="section-head">\s*<span class="icon">[^<]*</span>\s*<h2>([^<]+)</h2>\s*</div>\s*'
        r'<div class="charter-body">(.*?)</div>\s*</section>',
        text,
        re.DOTALL,
    )

    body_stats = []
    for sid, sep_title, art_label, body in sections:
        body_stats.append({
            "id": sid,
            "separate_title": sep_title.replace("<br/>", " / ").strip(),
            "article_label": art_label.strip(),
            "p": len(re.findall(r"<p[^>]*>", body)),
            "ol": len(re.findall(r"<ol[^>]*>", body)),
            "ul": len(re.findall(r"<ul[^>]*>", body)),
            "li": len(re.findall(r"<li[^>]*>", body)),
            "h3": len(re.findall(r"<h3[^>]*>", body)),
            "h3_texts": re.findall(r"<h3[^>]*>([^<]+)</h3>", body),
            "body_len": len(body.strip()),
        })

    return {
        "lines": len(lines),
        "chars": len(text),
        "html_attrs": (html_attrs.group(1).strip() if html_attrs else ""),
        "title": title.group(1) if title else "",
        "meta_desc": meta_descs[0] if meta_descs else "(none)",
        "og_title": og_title[0] if og_title else "(none)",
        "og_desc": og_desc[0] if og_desc else "(none)",
        "css_links": css_links,
        "scripts": scripts,
        "widget_title": widget_title.group(1).strip() if widget_title else "(none)",
        "toc_items": toc_items,
        "sections": body_stats,
        "section_count": len(body_stats),
    }


az = extract_structure(ROOT / "az" / "charter.html")
en = extract_structure(ROOT / "en" / "charter.html")

print("=== META / HEAD ===")
print(f'AZ html attrs: {az["html_attrs"]}')
print(f'EN html attrs: {en["html_attrs"]}')
print(f'AZ title: {az["title"]}')
print(f'EN title: {en["title"]}')
print(f'AZ meta-desc: {az["meta_desc"]}')
print(f'EN meta-desc: {en["meta_desc"]}')
print(f'AZ og:title:  {az["og_title"]}')
print(f'EN og:title:  {en["og_title"]}')
print(f'AZ og:desc:   {az["og_desc"]}')
print(f'EN og:desc:   {en["og_desc"]}')

print("\n=== ASSETS ===")
print(f'AZ CSS ({len(az["css_links"])}):')
for u in az["css_links"]:
    print(f"   {u}")
print(f'EN CSS ({len(en["css_links"])}):')
for u in en["css_links"]:
    print(f"   {u}")
print(f'AZ JS  ({len(az["scripts"])}):')
for u in az["scripts"]:
    print(f"   {u}")
print(f'EN JS  ({len(en["scripts"])}):')
for u in en["scripts"]:
    print(f"   {u}")

print("\n=== SIDEBAR ===")
print(f'AZ widget title: {az["widget_title"]}')
print(f'EN widget title: {en["widget_title"]}')
print(f'AZ TOC items: {len(az["toc_items"])}, EN TOC items: {len(en["toc_items"])}')

print("\n=== TOC LABELS ===")
for (a, b) in zip(az["toc_items"], en["toc_items"]):
    print(f'  {a[1]:<14} AZ[{a[0]:>4}] {a[2]}')
    print(f'  {b[1]:<14} EN[{b[0]:>4}] {b[2]}')

print("\n=== SECTION COUNTS ===")
print(f'AZ sections: {az["section_count"]}  EN sections: {en["section_count"]}')

print("\n=== PER-SECTION STRUCTURE ===")
print(f'{"id":<12}{"AZ p/ol/ul/li/h3":<22}{"EN p/ol/ul/li/h3":<22}  Δlen')
for a, b in zip(az["sections"], en["sections"]):
    az_sig = f'{a["p"]}/{a["ol"]}/{a["ul"]}/{a["li"]}/{a["h3"]}'
    en_sig = f'{b["p"]}/{b["ol"]}/{b["ul"]}/{b["li"]}/{b["h3"]}'
    marker = "" if az_sig == en_sig else "  STRUCT_DIFF"
    print(
        f'{a["id"]:<12}{az_sig:<22}{en_sig:<22}'
        f'  Δ={b["body_len"]-a["body_len"]:+d}{marker}'
    )

print("\n=== SECTION TITLES ===")
for a, b in zip(az["sections"], en["sections"]):
    print(f'  {a["id"]}')
    print(f'    AZ sep-title : {a["separate_title"]}')
    print(f'    EN sep-title : {b["separate_title"]}')
    print(f'    AZ h2        : {a["article_label"]}')
    print(f'    EN h2        : {b["article_label"]}')

print("\n=== SUB-HEADINGS (<h3>) ===")
for a, b in zip(az["sections"], en["sections"]):
    if a["h3_texts"] or b["h3_texts"]:
        print(f'  {a["id"]}:  AZ={len(a["h3_texts"])}  EN={len(b["h3_texts"])}')
        for txt in a["h3_texts"]:
            print(f"    AZ h3: {txt}")
        for txt in b["h3_texts"]:
            print(f"    EN h3: {txt}")
