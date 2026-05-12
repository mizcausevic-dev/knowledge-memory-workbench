from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PORT = "4562"


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    env = os.environ.copy()
    env["PORT"] = PORT
    process = subprocess.Popen(
        ["py", "-3.11", "-m", "app.main"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        time.sleep(2.5)
        if process.poll() is not None:
            stdout, stderr = process.communicate(timeout=2)
            raise RuntimeError(f"service exited before startup\nstdout:\n{stdout}\nstderr:\n{stderr}")

        root = get_json(f"http://127.0.0.1:{PORT}/")
        docs = get_json(f"http://127.0.0.1:{PORT}/docs")
        summary = get_json(f"http://127.0.0.1:{PORT}/api/dashboard/summary")
        sample = get_json(f"http://127.0.0.1:{PORT}/api/sample")

        req = urllib.request.Request(
            f"http://127.0.0.1:{PORT}/api/analyze/retrieval",
            data=json.dumps(
                {
                    "prompt": "Need board pipeline retention model briefing recovery",
                    "freshness_budget_days": 7,
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            analysis = json.loads(response.read().decode("utf-8"))

        assert root["service"] == "knowledge-memory-workbench"
        assert docs["routes"][0]["path"] == "/"
        assert summary["memory_packets"] == 18
        assert sample["id"] == "mem-101"
        assert analysis["top_packet"]["id"] == "mem-101"
        print("smoke_check: ok")
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


if __name__ == "__main__":
    main()

