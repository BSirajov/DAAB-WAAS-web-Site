import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "cv" / "bakhtiyar_sirajov_cv.html"
text = p.read_text(encoding="utf-8")
new_img = (
    '<img src="/images/bakhtiyar-sirajov.png" alt="Bakhtiyar Sirajov" '
    'width="160" height="200" loading="eager" />'
)
text2, n = re.subn(r'<img src="data:image[^"]+"[^/]*/>', new_img, text, count=1)
if not n:
    raise SystemExit("base64 img not found")
p.write_text(text2, encoding="utf-8")
print("ok", p)
