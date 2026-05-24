"""Strip obsolete daab-profile-card-layout block; bump scientists-profile-qr.css version."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from helpers._paths import AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES

QR_VERSION = 9
LAYOUT_BLOCK = re.compile(
    r'<style id="daab-profile-card-layout">.*?</style>\s*',
    re.DOTALL,
)


def inject(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"scientists-profile-qr\.css\?v=\d+",
        f"scientists-profile-qr.css?v={QR_VERSION}",
        text,
        count=1,
    )
    if LAYOUT_BLOCK.search(text):
        text = LAYOUT_BLOCK.sub("", text)
        print(f"removed layout block: {path.relative_to(ROOT)}")
    else:
        print(f"ok (no layout block): {path.relative_to(ROOT)}")
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    for p in (AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES):
        inject(p)


if __name__ == "__main__":
    main()
