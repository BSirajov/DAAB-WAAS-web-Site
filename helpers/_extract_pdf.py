from pypdf import PdfReader

from _paths import ROOT

pdf = ROOT / "documents/Forum_haqqinda_kitab_ (27.04.2026).pdf"
reader = PdfReader(str(pdf))
print("pages", len(reader.pages))

full = []
for i, page in enumerate(reader.pages):
    text = page.extract_text() or ""
    full.append(f"\n--- PAGE {i+1} ---\n{text}")

out = ROOT / "_pdf_extract.txt"
out.write_text("\n".join(full), encoding="utf-8")
print("written", out, "chars", out.stat().st_size)

# find chapter
text_all = "\n".join(full)
idx = text_all.lower().find("xaricdə")
print("chapter hits:", [text_all.lower().find(x) for x in ["xaricdə yaşayan", "xaricde yasayan", "azərbaycanlı alimlər"]])
