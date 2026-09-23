#!/usr/bin/env python3
"""Static preview server with gzip compression and cache headers."""
from __future__ import annotations

import argparse
import gzip
import io
import mimetypes
import socket
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

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
}


class DAABRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=directory or str(ROOT), **kwargs)

    def end_headers(self) -> None:
        path = self.path.split("?", 1)[0].lower()
        suffix = Path(path).suffix
        if suffix in LONG_CACHE_SUFFIXES:
            self.send_header("Cache-Control", "public, max-age=604800, immutable")
        elif suffix in (".html", ".json") or path.endswith("/"):
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


def port_in_use(host: str, port: int) -> bool:
    family = socket.AF_INET6 if ":" in host.strip("[]") else socket.AF_INET
    sock = socket.socket(family, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    try:
        target = host.strip("[]")
        return sock.connect_ex((target, port)) == 0
    finally:
        sock.close()


def preview_ok(host: str, port: int) -> bool:
    """True if this repo's Azerbaijani home page is being served."""
    url = f"http://{host}:{port}/az/index.html"
    try:
        with urlopen(url, timeout=0.8) as resp:
            body = resp.read().decode("utf-8", "replace")
            return resp.status == 200 and "primaryNavMenu" in body
    except (URLError, OSError, TimeoutError):
        return False


class ThreadingHTTPServerV6(ThreadingHTTPServer):
    address_family = socket.AF_INET6


def idle_until_interrupt() -> None:
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\nStopped.")


def main() -> None:
    parser = argparse.ArgumentParser(description="DAAB static site preview server")
    parser.add_argument("--port", type=int, default=8010)
    parser.add_argument("--bind", default="127.0.0.1")
    args = parser.parse_args()

    mimetypes.add_type("image/webp", ".webp")
    mimetypes.add_type("font/woff2", ".woff2")

    ipv4_ok = preview_ok("127.0.0.1", args.port)
    ipv6_ok = preview_ok("[::1]", args.port)
    # Windows resolves localhost to ::1 first; require both loopbacks when we bind IPv4.
    want_ipv6 = args.bind in ("127.0.0.1", "localhost")
    healthy = ipv4_ok and (ipv6_ok if want_ipv6 else True)

    # Reuse an already-running preview (VS Code F5 / START-SITE.bat) instead of crashing.
    if healthy:
        extra = " + http://[::1]" if ipv6_ok else ""
        print(
            f"Serving HTTP on {args.bind} port {args.port}{extra} "
            f"(already running, {ROOT}) ...",
            flush=True,
        )
        idle_until_interrupt()
        return

    if (
        port_in_use(args.bind, args.port)
        or port_in_use("127.0.0.1", args.port)
        or (want_ipv6 and port_in_use("::1", args.port))
    ):
        print(
            f"Port {args.port} is in use but is not serving this DAAB site "
            f"({ROOT}/az/index.html). Stop the other listener or run START-SITE.bat.",
            file=sys.stderr,
            flush=True,
        )
        raise SystemExit(1)

    servers: list[tuple[str, ThreadingHTTPServer]] = []
    servers.append((args.bind, ThreadingHTTPServer((args.bind, args.port), DAABRequestHandler)))
    if want_ipv6:
        try:
            servers.append(("::1", ThreadingHTTPServerV6(("::1", args.port), DAABRequestHandler)))
        except OSError as exc:
            print(f"(IPv6 ::1 not bound, localhost may fail: {exc})", flush=True)

    bound = ", ".join(f"{host}:{args.port}" for host, _ in servers)
    print(
        f"Serving HTTP on {bound} ({ROOT}, gzip + cache headers) ...",
        flush=True,
    )
    try:
        for _host, extra in servers[1:]:
            threading.Thread(target=extra.serve_forever, daemon=True).start()
        servers[0][1].serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        for _host, srv in servers:
            srv.shutdown()


if __name__ == "__main__":
    main()
