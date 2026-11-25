import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyse_events import analyse_events, validate_event


class TestEventValidation(unittest.TestCase):
    def setUp(self):
        self.valid_event = {
            "timestamp": "2026-11-25T08:10:00Z",
            "host": "WS-TEST-01",
            "channel": "Security",
            "event_id": 4624,
        }

    def test_valid_event(self):
        self.assertIsNone(validate_event(self.valid_event))

    def test_missing_host(self):
        event = self.valid_event.copy()
        del event["host"]
        self.assertEqual(
            validate_event(event),
            "Missing required field: host",
        )

    def test_invalid_timestamp(self):
        event = self.valid_event.copy()
        event["timestamp"] = "not-a-timestamp"
        self.assertEqual(
            validate_event(event),
            "Invalid timestamp format",
        )

    def test_invalid_event_id_type(self):
        event = self.valid_event.copy()
        event["event_id"] = "4624"
        self.assertEqual(
            validate_event(event),
            "Invalid event_id: expected integer",
        )

    def test_analyse_events_quarantines_malformed_lines(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sample_path = Path(tmpdir) / "events.jsonl"
            lines = [
                json.dumps(self.valid_event),
                "{bad json line",
                json.dumps({
                    "timestamp": "2026-11-25T08:11:00Z",
                    "host": "WS-TEST-01",
                    "event_id": 4625,
                }),
            ]
            sample_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

            summary = analyse_events(sample_path)
            self.assertEqual(summary["total_valid_records"], 1)
            self.assertEqual(summary["total_invalid_records"], 2)
            self.assertEqual(summary["successful_logons"], 1)


if __name__ == "__main__":
    unittest.main()
