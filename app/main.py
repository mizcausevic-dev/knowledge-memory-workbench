from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from app.services.memory_engine import MemoryEngine


PORT = int(os.environ.get("PORT", "4562"))


class Handler(BaseHTTPRequestHandler):
    def _write(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            self._write(
                {
                    "service": "knowledge-memory-workbench",
                    "status": "ok",
                    "docs": "/docs",
                    "dashboard": "/api/dashboard/summary",
                }
            )
            return

        if path == "/docs":
            self._write(
                {
                    "routes": [
                        {"method": "GET", "path": "/"},
                        {"method": "GET", "path": "/docs"},
                        {"method": "GET", "path": "/api/dashboard/summary"},
                        {"method": "GET", "path": "/api/packets"},
                        {"method": "GET", "path": "/api/packets/:id"},
                        {"method": "GET", "path": "/api/sample"},
                        {"method": "POST", "path": "/api/analyze/retrieval"},
                    ]
                }
            )
            return

        if path == "/api/dashboard/summary":
            self._write(MemoryEngine.summary())
            return

        if path == "/api/packets":
            self._write({"items": MemoryEngine.packets()})
            return

        if path == "/api/sample":
            self._write(MemoryEngine.sample_packet())
            return

        if path.startswith("/api/packets/"):
            packet_id = path.split("/")[-1]
            packet = MemoryEngine.packet_by_id(packet_id)
            if packet is None:
                self._write({"error": "packet not found"}, 404)
            else:
                self._write(packet)
            return

        self._write({"error": "not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path != "/api/analyze/retrieval":
            self._write({"error": "not found"}, 404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        try:
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self._write({"error": "invalid json"}, 400)
            return

        self._write(MemoryEngine.evaluate(payload))

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def main() -> None:
    try:
        server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        print(f"Knowledge Memory Workbench could not start because port {PORT} is already in use.")
        print('Set a different port before running again, for example:')
        print('$env:PORT = "4566"')
        print('py -3.11 -m app.main')
        raise SystemExit(1) from None

    print(f"Knowledge Memory Workbench running on http://127.0.0.1:{PORT}")
    print(f"Docs: http://127.0.0.1:{PORT}/docs")
    server.serve_forever()


if __name__ == "__main__":
    main()

