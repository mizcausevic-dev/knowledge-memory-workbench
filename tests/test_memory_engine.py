import unittest

from app.services.memory_engine import MemoryEngine


class MemoryEngineTest(unittest.TestCase):
    def test_summary_counts(self):
        summary = MemoryEngine.summary()
        self.assertEqual(summary["memory_packets"], 18)
        self.assertEqual(summary["stale_notes"], 3)
        self.assertEqual(summary["recovery_risk"], 2)

    def test_retrieval_prefers_relevant_packet(self):
        result = MemoryEngine.evaluate(
            {
                "prompt": "Need board pipeline retention model briefing recovery",
                "freshness_budget_days": 7,
            }
        )
        self.assertIn(result["status"], {"ready", "watch"})
        self.assertEqual(result["top_packet"]["id"], "mem-101")


if __name__ == "__main__":
    unittest.main()

