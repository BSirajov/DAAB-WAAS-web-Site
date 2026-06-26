#!/usr/bin/env python3
"""Extract and optionally HTTP-check external links in activities pages."""
from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from _paths import ROOT

ACTIVITIES_PAGES = (
    ROOT / "az" / "activities.html",
    ROOT / "en" / "activities.html",
)

HREF_RE = re.compile(
    r'<a\b[^>]*\bhref="(https?://[^"#]+)"',
    re.I,
)

SKIP_HOST_SUFFIXES = (
    "daab-waas.com",
    "localhost",
    "127.0.0.1",
)

USER_AGENT = "DAAB-Link-Checker/1.0 (+https://daab-waas.com)"


def extract_external_urls(html: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for match in HREF_RE.finditer(html):
        url = match.group(1).strip()
        host = re.sub(r"^https?://", "", url, flags=re.I).split("/")[0].lower()
        if any(host == suffix or host.endswith("." + suffix) for suffix in SKIP_HOST_SUFFIXES):
            continue
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def check_url(url: str, *, timeout: float) -> tuple[int | None, str]:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, ""
    except urllib.error.HTTPError as exc:
        if exc.code in (405, 501):
            return _get_status(url, timeout)
        return exc.code, str(exc.reason)
    except Exception as exc:  # noqa: BLE001 — report any network failure
        return _get_status(url, timeout, fallback_error=str(exc))


def _get_status(url: str, timeout: float, fallback_error: str = "") -> tuple[int | None, str]:
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, ""
    except urllib.error.HTTPError as exc:
        return exc.code, str(exc.reason)
    except Exception as exc:  # noqa: BLE001
        return None, fallback_error or str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Perform live HTTP checks (slow; requires network)",
    )
    parser.add_argument("--timeout", type=float, default=12.0, help="Per-URL timeout seconds")
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Exit 1 when any URL fails the live check",
    )
    args = parser.parse_args()

    all_urls: dict[str, list[str]] = {}
    for path in ACTIVITIES_PAGES:
        if not path.is_file():
            print(f"ERROR missing page: {path.relative_to(ROOT)}")
            return 1
        rel = path.relative_to(ROOT).as_posix()
        all_urls[rel] = extract_external_urls(path.read_text(encoding="utf-8"))

    unique = sorted({url for urls in all_urls.values() for url in urls})
    print(f"Activities external links — {len(unique)} unique URL(s) across {len(all_urls)} page(s)\n")
    for rel, urls in all_urls.items():
        print(f"  {rel}: {len(urls)} link(s)")

    if not args.check:
        print("\nList mode only (no network). Run with --check to verify HTTP status.")
        for url in unique:
            print(f"  {url}")
        return 0

    print("\nLive HTTP check:")
    failures: list[tuple[str, int | None, str]] = []
    for url in unique:
        status, err = check_url(url, timeout=args.timeout)
        if status is None or status >= 400:
            failures.append((url, status, err))
            label = f"FAIL ({status})" if status else "FAIL"
            print(f"  {label}: {url}")
            if err:
                print(f"         {err}")
        else:
            print(f"  OK {status}: {url}")

    if failures:
        print(f"\n{len(failures)} of {len(unique)} URL(s) failed.")
        return 1 if args.fail_on_error else 0

    print(f"\nOK — all {len(unique)} URL(s) responded successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
