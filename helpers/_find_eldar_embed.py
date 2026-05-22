"""Find docx image linked to Eldar Əhədov profile."""
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "documents" / "Forum_haqqinda_kitab_ (24.04.2026_4.0).docx"

with zipfile.ZipFile(DOCX) as z:
    rels_xml = z.read("word/_rels/document.xml.rels").decode("utf-8")
    doc_xml = z.read("word/document.xml").decode("utf-8")

# rId -> filename
id_to_file = {}
for m in re.finditer(
    r'Id="(rId\d+)"[^>]*Target="media/([^"]+)"', rels_xml
):
    id_to_file[m.group(1)] = m.group(2)

print("rels", len(id_to_file))

# All drawings in document order with nearby text snippet
parts = re.split(r"(<w:drawing>)", doc_xml)
drawings = []
pos = 0
for i, part in enumerate(parts):
    pos += len(part)
    if part == "<w:drawing>":
        # get next chunk until </w:drawing>
        chunk = parts[i + 1] if i + 1 < len(parts) else ""
        end = chunk.find("</w:drawing>")
        block = part + chunk[: end + len("</w:drawing>")] if end >= 0 else part + chunk[:4000]
        embed = re.search(r'r:embed="(rId\d+)"', block)
        if embed:
            rid = embed.group(1)
            fname = id_to_file.get(rid, "?")
            # text before this drawing (last 500 chars stripped of tags)
            before = re.sub(r"<[^>]+>", " ", doc_xml[max(0, pos - 6000) : pos])
            before = re.sub(r"\s+", " ", before).strip()[-200:]
            drawings.append((fname, before))

print("drawings", len(drawings))
for fname, before in drawings:
    if "Eldar" in before or "ƏHƏDOV" in before or "Əhədov" in before:
        print("---", fname)
        print(before)

# Also list drawings 44-50 by order
print("\norder 44-50:")
for j, (fname, before) in enumerate(drawings[43:50], start=44):
    print(j, fname, "|", before[:120])

# Scientist chapter: search by readable name fragments
for fname, before in drawings:
    clean = re.sub(r"[^A-Za-zƏəŞşÇçĞğÖöÜüİı\s]", " ", before)
    if re.search(r"Eldar|Əliheydər|ƏHƏDOV|RƏHİMOV", clean):
        if "FORUMLA" not in clean and "HEKAY" not in clean:
            print("NAME?", fname, "|", clean[-150:])
