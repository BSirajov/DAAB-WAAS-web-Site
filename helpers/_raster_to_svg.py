#!/usr/bin/env python3
"""Convert raster logos to SVG using vtracer (run from repo root)."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from _paths import ROOT

try:
    import vtracer
except ImportError:
    print("Install vtracer: pip install vtracer", file=sys.stderr)
    raise

IMAGES = ROOT / "images"

# (source relative to ROOT or absolute, output SVG name)
CURSOR_ASSETS = Path(
    r"C:\Users\BSira\.cursor\projects\c-Users-BSira-Documents-GitHub-DAAB-WAAS-web-site\assets"
)

JOBS: list[tuple[Path, str]] = [
    (IMAGES / "DİDK Loqo.jpg", "didk-emblem.svg"),
    (IMAGES / "ETN.png", "etn-logo.svg"),
    (CURSOR_ASSETS / "c__Users_BSira_AppData_Roaming_Cursor_User_workspaceStorage_419ddc31f2527d207d33d608c6ef814c_images_D_DK_Loqo-d5608bc9-a279-4e9a-b3f9-b09c815b2a06.png", "didk-emblem.svg"),
    (CURSOR_ASSETS / "c__Users_BSira_AppData_Roaming_Cursor_User_workspaceStorage_419ddc31f2527d207d33d608c6ef814c_images_ETN-82741ef6-eca8-43f6-8987-880fe16ac94c.png", "etn-logo.svg"),
]


def ensure_png(src: Path, work_dir: Path) -> Path:
    """vtracer accepts jpg/png; normalize to png in work dir for stable names."""
    if src.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        if src.suffix.lower() == ".png":
            dest = work_dir / f"{src.stem}.png"
            if src.resolve() != dest.resolve():
                shutil.copy2(src, dest)
            return dest
        try:
            from PIL import Image
        except ImportError:
            return src
        dest = work_dir / f"{src.stem}.png"
        Image.open(src).convert("RGBA").save(dest, "PNG")
        return dest
    return src


def convert_one(src: Path, out_name: str, work_dir: Path) -> Path | None:
    if not src.is_file():
        return None
    inp = ensure_png(src, work_dir)
    out = IMAGES / out_name
    vtracer.convert_image_to_svg_py(
        str(inp),
        str(out),
        colormode="color",
        hierarchical="stacked",
        mode="spline",
        filter_speckle=4,
        color_precision=8,
        layer_difference=12,
        path_precision=4,
    )
    return out


def main() -> None:
    work = ROOT / "helpers" / "_svg_work"
    work.mkdir(parents=True, exist_ok=True)
    done: set[str] = set()
    for src, out_name in JOBS:
        if out_name in done:
            continue
        result = convert_one(src, out_name, work)
        if result:
            done.add(out_name)
            size_kb = result.stat().st_size / 1024
            print(f"Wrote {result.relative_to(ROOT)} ({size_kb:.1f} KB)")
        else:
            print(f"Skip missing: {src}")
    if not done:
        sys.exit(1)


if __name__ == "__main__":
    main()
