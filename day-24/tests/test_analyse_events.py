import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from analyse_events import analyse_events, validate_event


class TestEventValidationAndAnalysis(unittest.TestCase):
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

    def test_chronological_sorting_and_event_groupings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sample_path = Path(tmpdir) / "shuffled_ws_fin_04.jsonl"
            # Intentionally written out of chronological order
            unordered_events = [
                {
                    "timestamp": "2026-11-25T09:10:00Z",
                    "host": "WS-FIN-04",
                    "channel": "Security",
                    "event_id": 1102,
                    "username": "user_a",
                },
                {
                    "timestamp": "2026-11-25T09:03:00Z",
                    "host": "WS-FIN-04",
                    "channel": "Security",
                    "event_id": 4624,
                    "username": "user_a",
                    "source_ip": "203.0.113.45",
                },
                {
                    "timestamp": "2026-11-25T09:01:00Z",
                    "host": "WS-FIN-04",
                    "channel": "Security",
                    "event_id": 4625,
                    "username": "user_a",
                    "source_ip": "203.0.113.45",
                },
                {
                    "timestamp": "2026-11-25T09:05:00Z",
                    "host": "WS-FIN-04",
                    "channel": "Sysmon",
                    "event_id": 3,
                    "username": "user_a",
                    "process_name": "sample.exe",
                    "destination_ip": "198.51.100.70",
                },
                {
                    "timestamp": "2026-11-25T09:04:00Z",
                    "host": "WS-FIN-04",
                    "channel": "Sysmon",
                    "event_id": 1,
                    "username": "user_a",
                    "process_name": "sample.exe",
                    "parent_process": "explorer.exe",
                },
            ]
            sample_path.write_text(
                "\n".join(json.dumps(ev) for ev in unordered_events) + "\n",
                encoding="utf-8",
            )

            summary = analyse_events(sample_path)
            timestamps = [ev["timestamp"] for ev in summary["timeline"]]
            self.assertEqual(
                timestamps,
                [
                    "2026-11-25T09:01:00Z",
                    "2026-11-25T09:03:00Z",
                    "2026-11-25T09:04:00Z",
                    "2026-11-25T09:05:00Z",
                    "2026-11-25T09:10:00Z",
                ],
            )
            self.assertEqual(
                [ev["event_id"] for ev in summary["logon_sequence"]],
                [4625, 4624],
            )
            self.assertEqual(
                [ev["event_id"] for ev in summary["process_and_network_events"]],
                [1, 3],
            )
            self.assertEqual(
                [ev["event_id"] for ev in summary["audit_log_cleared_events"]],
                [1102],
            )



    def test_fixture_out_of_order_file_sorts_chronologically(self):
        fixture_path = Path(__file__).resolve().parent / "fixtures" / "out_of_order_events.jsonl"
        summary = analyse_events(fixture_path)
        self.assertEqual(
            [ev["timestamp"] for ev in summary["timeline"]],
            [
                "2026-11-25T09:01:00Z",
                "2026-11-25T09:03:00Z",
                "2026-11-25T09:05:00Z",
            ],
        )


if __name__ == "__main__":
    unittest.main()
