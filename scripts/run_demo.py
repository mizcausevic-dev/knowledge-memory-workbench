from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.memory_engine import MemoryEngine


def main() -> None:
    runtime = ROOT / "runtime"
    runtime.mkdir(exist_ok=True)
    report = MemoryEngine.evaluate(
        {
            "prompt": "Need board pipeline retention model briefing recovery",
            "freshness_budget_days": 7,
        }
    )
    path = runtime / "demo_report.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Knowledge Memory Workbench demo report")
    print(json.dumps({"status": report["status"], "top_packet": report["top_packet"]["id"]}, indent=2))
    print(f"Report written to: {path}")


if __name__ == "__main__":
    main()
