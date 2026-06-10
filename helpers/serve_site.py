#!/usr/bin/env python3
"""Static preview server with gzip compression and cache headers."""
from __future__ import annotations

import argparse
import gzip
import io
import mimetypes
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from _paths import ROOT

COMPRESSIBLE_SUFFIXES = {
    ".html",
    ".css",
    ".js",
    ".json",
    ".svg",
    ".xml",
    ".txt",
    ".map",
}

LONG_CACHE_SUFFIXES = {
    ".css",
    ".js",
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".svg",
    ".ico",
    ".woff",
    ".woff2",
    ".json",
}


class DAABRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=directory or str(ROOT), **kwargs)

    def end_headers(self) -> None:
        path = self.path.split("?", 1)[0].lower()
        suffix = Path(path).suffix
        if suffix in LONG_CACHE_SUFFIXES:
            self.send_header("Cache-Control", "public, max-age=604800, immutable")
        elif suffix == ".html" or path.endswith("/"):
            self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        file_path = Path(path)
        if not file_path.is_file():
            return super().send_head()

        ctype = self.guess_type(path)
        suffix = file_path.suffix.lower()
        accept_encoding = self.headers.get("Accept-Encoding", "")
        use_gzip = "gzip" in accept_encoding and suffix in COMPRESSIBLE_SUFFIXES

        try:
            with open(file_path, "rb") as fh:
                data = fh.read()
        except OSError:
            self.send_error(404, "File not found")
            return None

        if use_gzip:
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=6) as gz:
                gz.write(data)
            payload = buf.getvalue()
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Vary", "Accept-Encoding")
            self.end_headers()
            return io.BytesIO(payload)

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        return io.BytesIO(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="DAAB static site preview server")
    parser.add_argument("--port", type=int, default=8010)
    parser.add_argument("--bind", default="127.0.0.1")
    args = parser.parse_args()

    mimetypes.add_type("image/webp", ".webp")
    mimetypes.add_type("font/woff2", ".woff2")

    server = ThreadingHTTPServer((args.bind, args.port), DAABRequestHandler)
    print(f"Serving {ROOT} at http://{args.bind}:{args.port}/ (gzip + cache headers)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
