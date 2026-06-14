#!/usr/bin/env python3
"""Extract infographic text from invention card images and crop subject icons."""
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image
from rapidocr_onnxruntime import RapidOCR

from _paths import ROOT

PREVIEW_DIR = ROOT / "documents" / "preview"
IMAGE_DIR = PREVIEW_DIR / "images"
ICON_DIR = IMAGE_DIR / "icons"
CARD_DATA = PREVIEW_DIR / "inventions-card-data.json"

CARD_W = 857
CARD_H = 308
HEADER_H = 68
# Fixed illustration column from the 857×308 card template (text begins ~x198).
ICON_BOX = (48, 100, 182, 296)
TEXT_BOX = (198, 70, 845, 298)
TEXT_SPLIT_X = 545
OCR_SCALE = 4

FACT_PREFIXES = (
    "oldest evidence",
    "first use",
    "first ",
    "key sites",
    "cooking ",
    "enabled ",
    "precursor ",
    "transport ",
    "americas",
    "rotary ",
    "spindle",
    "turing test",
    "turing ",
    "alexnet",
    "alphafold",
    "artificial intelligence",
    "'artificial",
    "llms",
    "gpt",
    "rank",
    "mass ",
    "added ",
    "antimicrobial",
    "~",
    "c.",
)

OCR_FIXES = (
    (r"\bhumanbiology\b", "human biology"),
    (r"\bsettlementin\b", "settlement in"),
    (r"\bcolderclimates\b", "colder climates"),
    (r"\bWonderwerkCave\b", "Wonderwerk Cave"),
    (r"\bHomoerectus\b", "Homo erectus"),
    (r"\bHomosapiens\b", "Homo sapiens"),
    (r"\bSouthAfrica\b", "South Africa"),
    (r"\b~1 M rs ago\b", "~1 million years ago"),
    (r"\b~1M\b", "~1 million years"),
    (r"\bAlex Net\b", "AlexNet"),
    (r"\bAlpha Fold\b", "AlphaFold"),
    (r"\bprotection-\s*reshaping\b", "protection — reshaping"),
    (r"\btection-\s*reshaping\b", "protection — reshaping"),
    (r"\btection\s*-\s*reshaping\b", "protection — reshaping"),
    (r"\bvears\b", "years"),
    (r"\baoo\b", "ago"),
    (r"\blearming\b", "learning"),
    (r"\blerpins\b", "underpins"),
    (r"\bFirstuse\b", "First use"),
    (r"\bAmericasand\b", "Americas and"),
    (r"\bAfricadevelopedwithoutit\b", "Africa developed without it"),
    (r"\bArtificialintelligence\b", "Artificial intelligence"),
    (r"\bs the axle\b", "was the axle"),
    (r"\bkey insight s\b", "key insight was"),
    (r"\bwheel appeared\b", "The wheel appeared"),
    (r"\bep learning\b", "Deep learning"),
    (r"\bdem AI era\b", "modern AI era"),
    (r"\bAlera\b", "AI era"),
    (r"\b50-yearprotein\b", "50-year protein"),
    (r"\bsolvedprotein\b", "solved protein"),
    (r"\bMc Carthy\b", "McCarthy"),
    (r"\bn Tuning\b", "Turing"),
    (r"\s{2,}", " "),
)


def restore_spaces(text: str) -> str:
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text)
    text = re.sub(r"(\d)([A-Za-z])", r"\1 \2", text)
    text = re.sub(r";\s*", "; ", text)
    text = re.sub(r",\s*", ", ", text)
    text = re.sub(r":\s*", ": ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def proofread(text: str) -> str:
    for pattern, repl in OCR_FIXES:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    text = text.replace(" ,", ",").replace(" .", ".")
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"([.!?])\s*([A-Z])", r"\1 \2", text)
    return text.strip()


def line_center_x(box: list) -> float:
    xs = [point[0] for point in box]
    return sum(xs) / len(xs)


def ocr_lines(ocr: RapidOCR, image: Image.Image, box: tuple[int, int, int, int], scale: int) -> list[dict]:
    crop = image.crop(box)
    if scale > 1:
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.LANCZOS)
    result, _ = ocr(crop)
    lines: list[dict] = []
    for item in result or []:
        box_pts, text, _score = item
        text = text.strip()
        if not text:
            continue
        cx = line_center_x(box_pts) / scale + box[0]
        cy = sum(point[1] for point in box_pts) / len(box_pts) / scale + box[1]
        lines.append({"text": text, "x": cx, "y": cy})
    lines.sort(key=lambda row: (round(row["y"] / 12), row["x"]))
    return lines


def is_fact_line(text: str, x: float) -> bool:
    lowered = text.lower()
    if x >= TEXT_SPLIT_X - 8:
        return True
    if lowered in {"key facts", "key fact", "keyfacts"}:
        return True
    return any(lowered.startswith(prefix) for prefix in FACT_PREFIXES)


def parse_key_figures(text: str) -> str:
    match = re.search(
        r"(?:Key figure\(s\)|figure\(s\))\s*:\s*(.+)",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return ""
    value = match.group(1).strip()
    value = re.split(r"\bKEY\s*FACTS?\b", value, flags=re.IGNORECASE)[0].strip(" .")
    value = re.split(r"\b(?:Yann|Yanrk|KEYFAC|ELFAC)\b", value, flags=re.IGNORECASE)[0].strip(" .;:")
    value = proofread(restore_spaces(value))
    if re.search(r"KEYFAC|ELFAC|Yanrk|Bengio$", value, flags=re.IGNORECASE):
        return ""
    return value


def merge_summary_parts(parts: list[str]) -> str:
    blob = " ".join(parts)
    blob = re.sub(r"^(?:evidence from|Fire evidence from)", "Fire evidence from", blob, flags=re.IGNORECASE)
    blob = re.sub(r"^rs ago\.\s*", "years ago. ", blob, flags=re.IGNORECASE)
    blob = re.sub(r"^tection-\s*", "protection — ", blob, flags=re.IGNORECASE)
    blob = restore_spaces(proofread(blob))
    if blob and not blob.endswith((".", "!", "?")):
        blob += "."
    return blob


def normalize_fact(text: str) -> str:
    text = restore_spaces(proofread(text))
    text = re.sub(r"^Key sites:\s*", "Key sites: ", text, flags=re.IGNORECASE)
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text


def parse_body_lines(lines: list[dict]) -> tuple[str, str, list[str]]:
    key_figures = ""
    summary_parts: list[str] = []
    facts: list[str] = []
    seen_facts: set[str] = set()

    for row in lines:
        text = row["text"]
        lowered = text.lower()
        if lowered in {"key facts", "keyfact", "key fact", "keyfacts"}:
            continue
        if not key_figures and re.search(r"figure\(s\)\s*:", text, flags=re.IGNORECASE):
            key_figures = parse_key_figures(text)
            continue
        if is_fact_line(text, row["x"]):
            fact = normalize_fact(text)
            key = fact.lower()
            if fact and key not in seen_facts and not re.match(r"^figure\(s\)", key):
                seen_facts.add(key)
                facts.append(fact)
            continue
        if lowered.startswith(("oldest ", "key sites", "cooking ", "enabled ", "precursor ")):
            fact = normalize_fact(text)
            key = fact.lower()
            if key not in seen_facts:
                seen_facts.add(key)
                facts.append(fact)
            continue
        summary_parts.append(text)

    summary = merge_summary_parts(summary_parts)
    return key_figures, summary, facts


def crop_icon(image: Image.Image, dest: Path) -> None:
    icon = image.crop(ICON_BOX)
    dest.parent.mkdir(parents=True, exist_ok=True)
    icon.save(dest, format="PNG", optimize=True)


def extract_card(slug: str, ocr: RapidOCR) -> dict:
    image = Image.open(IMAGE_DIR / f"{slug}.png").convert("RGB")
    crop_icon(image, ICON_DIR / f"{slug}.png")
    lines = ocr_lines(ocr, image, TEXT_BOX, OCR_SCALE)
    key_figures, summary, facts = parse_body_lines(lines)
    return {
        "slug": slug,
        "icon": f"images/icons/{slug}.png",
        "key_figures": key_figures,
        "summary": summary,
        "key_facts": facts[:6],
    }


def load_overrides() -> dict:
    override_path = PREVIEW_DIR / "inventions-card-overrides.json"
    if not override_path.exists():
        return {}
    return json.loads(override_path.read_text(encoding="utf-8"))


def merge_override(card: dict, override: dict) -> dict:
    if not override:
        return card
    merged = dict(card)
    for key in ("key_figures", "summary", "key_facts", "icon"):
        if override.get(key):
            merged[key] = override[key]
    return merged


def icons_only() -> int:
    count = 0
    for image_path in sorted(IMAGE_DIR.glob("*.png")):
        if image_path.parent.name == "icons":
            continue
        crop_icon(Image.open(image_path).convert("RGB"), ICON_DIR / f"{image_path.stem}.png")
        count += 1
    return count


def main() -> None:
    import sys

    if "--icons-only" in sys.argv:
        count = icons_only()
        print(f"Wrote {count} icons to {ICON_DIR.relative_to(ROOT)}")
        return

    ocr = RapidOCR()
    overrides = load_overrides()
    cards: dict[str, dict] = {}
    for image_path in sorted(IMAGE_DIR.glob("*.png")):
        if image_path.parent.name == "icons":
            continue
        slug = image_path.stem
        card = extract_card(slug, ocr)
        card = merge_override(card, overrides.get(slug, {}))
        cards[slug] = card
    CARD_DATA.write_text(json.dumps(cards, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {CARD_DATA.relative_to(ROOT)} ({len(cards)} cards)")


if __name__ == "__main__":
    main()
