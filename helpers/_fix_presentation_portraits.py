#!/usr/bin/env python3
"""Rebuild scientists-photos portraits with clean site background (#e8eef4)."""
from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

from _paths import ROOT

SITE_BG = (232, 238, 244)
OUT_SIZE = 480


def _distance_inside_mask(mask: np.ndarray, max_dist: int = 32) -> np.ndarray:
    """Manhattan distance from the mask silhouette edge inward."""
    h, w = mask.shape
    dist = np.zeros((h, w), dtype=np.int32)
    q: deque[tuple[int, int]] = deque()
    for y in range(h):
        for x in range(w):
            if not mask[y, x]:
                continue
            on_edge = False
            for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if ny < 0 or ny >= h or nx < 0 or nx >= w or not mask[ny, nx]:
                    on_edge = True
                    break
            if on_edge:
                dist[y, x] = 1
                q.append((y, x))
    while q:
        y, x = q.popleft()
        d = dist[y, x]
        if d >= max_dist:
            continue
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and dist[ny, nx] == 0:
                dist[ny, nx] = d + 1
                q.append((ny, nx))
    # Unreached interior (enclosed) — treat as deep inside the subject.
    dist[(mask) & (dist == 0)] = max_dist + 1
    return dist


def _flood_edges(mask: np.ndarray) -> np.ndarray:
    """True for mask pixels connected to any image border."""
    h, w = mask.shape
    seen = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()
    for x in range(w):
        for y in (0, h - 1):
            if mask[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    for y in range(1, h - 1):
        for x in (0, w - 1):
            if mask[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))
    return seen


def _luminance(rgb: np.ndarray) -> np.ndarray:
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return (0.299 * r + 0.587 * g + 0.114 * b).astype(np.float32)


def _saturation(rgb: np.ndarray) -> np.ndarray:
    mx = rgb.max(axis=2).astype(np.float32)
    mn = rgb.min(axis=2).astype(np.float32)
    delta = mx - mn
    with np.errstate(divide="ignore", invalid="ignore"):
        out = np.where(mx > 0, delta / mx, 0.0)
    return np.nan_to_num(out, nan=0.0)


def _border_opaque(alpha: np.ndarray) -> np.ndarray:
    opaque = alpha > 0
    up = np.zeros_like(opaque)
    down = np.zeros_like(opaque)
    left = np.zeros_like(opaque)
    right = np.zeros_like(opaque)
    up[1:] = opaque[:-1]
    down[:-1] = opaque[1:]
    left[:, 1:] = opaque[:, :-1]
    right[:, :-1] = opaque[:, 1:]
    return opaque & (~up | ~down | ~left | ~right)


def _keep_largest_component(alpha: np.ndarray) -> np.ndarray:
    """Drop stray cutout islands (common above the hair on bad masks)."""
    h, w = alpha.shape
    labels = np.zeros((h, w), dtype=np.int32)
    current = 0
    sizes: dict[int, int] = {}
    for y in range(h):
        for x in range(w):
            if alpha[y, x] == 0 or labels[y, x]:
                continue
            current += 1
            stack = [(y, x)]
            labels[y, x] = current
            count = 0
            while stack:
                cy, cx = stack.pop()
                count += 1
                for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                    if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx] and not labels[ny, nx]:
                        labels[ny, nx] = current
                        stack.append((ny, nx))
            sizes[current] = count
    if not sizes:
        return alpha
    keep = max(sizes, key=sizes.get)
    out = np.zeros_like(alpha)
    out[labels == keep] = alpha[labels == keep]
    return out


def _peel_light_fringe(alpha: np.ndarray, rgb: np.ndarray, passes: int = 32) -> np.ndarray:
    """Strip light halo layers working inward from the silhouette edge."""
    lum = _luminance(rgb)
    sat = _saturation(rgb)
    a = alpha.copy()
    for _ in range(passes):
        border = _border_opaque(a)
        peel = border & (
            (lum > 178.0)
            | ((lum > 138.0) & (sat < 0.11))
            | (rgb.min(axis=2) > 215)
            | (lum < 108.0)
        )
        if not peel.any():
            break
        a[peel] = 0
    return _keep_largest_component(a)


def _rgba_from_black_cutout(rgb: np.ndarray) -> np.ndarray:
    """Remove black studio background and light cutout halos."""
    dark = rgb.max(axis=2) < 42
    bg = _flood_edges(dark)
    subject = ~bg
    alpha = np.where(subject, 255, 0).astype(np.uint8)
    alpha = _peel_light_fringe(alpha, rgb)
    return np.dstack([rgb, alpha])


def _rgba_from_white_studio(rgb: np.ndarray) -> np.ndarray:
    """Keep subject on white studio background; do not flood through interior whites."""
    near_white = rgb.min(axis=2) > 246
    bg = _flood_edges(near_white)
    alpha = np.where(~bg, 255, 0).astype(np.uint8)
    return np.dstack([rgb, alpha])


def _square_crop_rgba(
    rgba: np.ndarray, headroom_top: float = 0.06, max_bottom_frac: float = 0.88
) -> np.ndarray:
    alpha = rgba[..., 3]
    ys, xs = np.where(alpha > 12)
    if ys.size == 0:
        return rgba
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())
    span = y1 - y0 + 1
    y1 = min(y1, y0 + int(span * max_bottom_frac))
    crop = rgba[y0 : y1 + 1, x0 : x1 + 1]
    fh, fw = crop.shape[:2]
    side = int(max(fw, fh) * 1.12)
    canvas = np.zeros((side, side, 4), dtype=np.uint8)
    ox = (side - fw) // 2
    oy = max(0, int((side - fh) * headroom_top))
    canvas[oy : oy + fh, ox : ox + fw] = crop
    return canvas


def _flatten_to_site_bg(rgba: np.ndarray, size: int = OUT_SIZE) -> Image.Image:
    im = Image.fromarray(rgba, mode="RGBA")
    im = im.resize((size, size), Image.Resampling.LANCZOS)
    bg = Image.new("RGB", (size, size), SITE_BG)
    bg.paste(im, mask=im.split()[3])
    return bg


def _face_tight_crop(rgba: np.ndarray) -> np.ndarray:
    """Drop rough shoulder fade; keep head-dominant framing for bad studio masks."""
    alpha = rgba[..., 3]
    ys, xs = np.where(alpha > 12)
    if ys.size == 0:
        return rgba
    y0, y1 = int(ys.min()), int(ys.max())
    x0, x1 = int(xs.min()), int(xs.max())
    fh, fw = y1 - y0 + 1, x1 - x0 + 1
    mx = x0 + int(fw * 0.08)
    my = y0 + int(fh * 0.02)
    mw = x0 + int(fw * 0.92)
    mh = y0 + int(fh * 0.82)
    return rgba[my : mh + 1, mx : mw + 1]


def _defringe_rgba(rgba: np.ndarray) -> np.ndarray:
    """Soften rembg edge halos before flattening to the site background."""
    rgb = rgba[..., :3]
    a = _peel_light_fringe(rgba[..., 3].copy(), rgb, passes=8)
    return np.dstack([rgb, a])


def _rembg_rgba(src: Path) -> np.ndarray | None:
    try:
        from rembg import remove
    except ImportError:
        return None
    cut = remove(Image.open(src))
    if cut.mode != "RGBA":
        cut = cut.convert("RGBA")
    return np.array(cut)


def _process_black_studio(src: Path, dest: Path) -> None:
    rgba = _rembg_rgba(src)
    if rgba is None:
        rgb = np.array(Image.open(src).convert("RGB"))
        rgba = _rgba_from_black_cutout(rgb)
    rgba = _face_tight_crop(_square_crop_rgba(rgba, max_bottom_frac=1.0))
    rgba = _defringe_rgba(rgba)
    out = _flatten_to_site_bg(rgba)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, "PNG", optimize=True)
    print(f"  {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes) <- {src.name}")


def _process_white_studio(src: Path, dest: Path) -> None:
    """Professional white-backdrop portraits: edge flood only (avoids rembg halos)."""
    rgb = np.array(Image.open(src).convert("RGB"))
    rgba = _rgba_from_white_studio(rgb)
    rgba = _square_crop_rgba(rgba)
    out = _flatten_to_site_bg(rgba)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, "PNG", optimize=True)
    print(f"  {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes) <- {src.name}")


def main() -> None:
    photos = ROOT / "images" / "scientists-photos"
    board = ROOT / "images" / "board-members-photos"

    # Asaf: use images/scientists-photos/asef-salamov.png as uploaded (do not reprocess).

    bakht_src = board / "bakhtiyar-sirajov.png"
    if not bakht_src.is_file():
        bakht_src = board / "bakhtiyar-sirajov 1.png"
    if not bakht_src.is_file():
        bakht_src = photos / "bakhtiyar-sirajov.png"

    print("Rebuilding presentation / profile portraits (Bakhtiyar only):")
    _process_white_studio(bakht_src, photos / "bakhtiyar-sirajov.png")


if __name__ == "__main__":
    main()
