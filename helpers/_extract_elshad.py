from pathlib import Path
src = Path(__file__).resolve().parent / "_build_elshad_cv.py"
text = src.read_text(encoding="utf-16-le")
marker = 'HTML = r"""'
start = text.index(marker) + len(marker)
end = text.rindex('"""')
html = text[start:end]
out = Path(__file__).resolve().parents[1] / "cv" / "elshad_allahyarov.html"
out.write_text(html, encoding="utf-8")
print(out, out.stat().st_size)
