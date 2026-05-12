from __future__ import annotations

from collections import Counter
from typing import Any

from app.data.sample_memory_data import SAMPLE_DATA


class MemoryEngine:
    @staticmethod
    def summary() -> dict[str, Any]:
        return SAMPLE_DATA["dashboard"]

    @staticmethod
    def packets() -> list[dict[str, Any]]:
        return SAMPLE_DATA["packets"]

    @staticmethod
    def sample_packet() -> dict[str, Any]:
        return SAMPLE_DATA["packets"][0]

    @staticmethod
    def packet_by_id(packet_id: str) -> dict[str, Any] | None:
        return next((packet for packet in SAMPLE_DATA["packets"] if packet["id"] == packet_id), None)

    @staticmethod
    def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
        prompt = str(payload.get("prompt", "")).lower()
        freshness_budget = int(payload.get("freshness_budget_days", 7))
        keyword_hits = Counter()
        scored = []

        for packet in SAMPLE_DATA["packets"]:
            keyword_score = sum(1 for keyword in packet["keywords"] if keyword in prompt)
            freshness_penalty = max(packet["freshness_days"] - freshness_budget, 0) * 0.9
            confidence_bonus = float(packet["confidence"]) * 10
            total = (keyword_score * 5) + confidence_bonus - freshness_penalty
            keyword_hits[packet["domain"]] += keyword_score
            scored.append(
                {
                    "id": packet["id"],
                    "title": packet["title"],
                    "domain": packet["domain"],
                    "freshness_days": packet["freshness_days"],
                    "score": round(total, 1),
                    "keyword_hits": keyword_score,
                    "staleness_risk": packet["staleness_risk"],
                }
            )

        ranked = sorted(scored, key=lambda item: (-item["score"], item["freshness_days"]))
        best = ranked[0]

        status = "recover"
        if best["score"] >= 16:
            status = "ready"
        elif best["score"] >= 10:
            status = "watch"

        next_action = {
            "ready": "Use the top packet as the anchor context and attach one fresh operator note before briefing distribution.",
            "watch": "Recover from the top packet, but refresh the stale lane and verify the owner before relying on it.",
            "recover": "Too much context is aging out. Trigger a capture pass and rebuild the memory lane before using it.",
        }[status]

        return {
            "status": status,
            "top_packet": best,
            "ranked_packets": ranked,
            "dominant_domain": keyword_hits.most_common(1)[0][0] if keyword_hits else "unknown",
            "next_action": next_action,
        }

