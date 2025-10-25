"""Launcher for Dungeon Keeper: Middle Management as a desktop app.

This script starts a lightweight HTTP server to serve the existing HTML/JS
frontend, then embeds it inside a native window using pywebview. It also
exposes a small bridge so the web code can load local JSON overrides without
running into browser CORS restrictions.
"""
from __future__ import annotations

import argparse
import json
import socket
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Tuple

import webview


def resource_root() -> Path:
    """Return the directory that contains the bundled web assets."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent


class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    """HTTP handler that serves from a given directory without noisy logs."""

    def __init__(self, *args, directory: str, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format: str, *args) -> None:  # noqa: A003 - inherited
        pass


class DesktopHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def start_server(root: Path) -> Tuple[DesktopHTTPServer, int]:
    """Start an HTTP server in a background thread and return it with its port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    handler = lambda *args, **kwargs: QuietHTTPRequestHandler(  # noqa: E731
        *args, directory=str(root), **kwargs
    )
    server = DesktopHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, port


class Bridge:
    """API exposed to the web frontend via pywebview."""

    def __init__(self, root: Path):
        self._root = root

    def loadJSON(self, rel_path: str):  # noqa: N802 - keep camelCase for JS parity
        """Load a JSON file shipped with the app and return its parsed content."""
        target = (self._root / rel_path).resolve()
        try:
            target.relative_to(self._root)
        except ValueError as exc:
            raise ValueError("Invalid path") from exc
        if not target.exists():
            return None
        with target.open("r", encoding="utf-8") as fh:
            return json.load(fh)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--title",
        default="Dungeon Keeper: Middle Management",
        help="Window title override.",
    )
    args = parser.parse_args()

    root = resource_root()
    server, port = start_server(root)
    bridge = Bridge(root)

    window = webview.create_window(
        args.title,
        url=f"http://127.0.0.1:{port}/index.html",
        js_api=bridge,
    )
    try:
        webview.start()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
