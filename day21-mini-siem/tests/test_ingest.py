import unittest
from src.normalizer import normalise_record

class TestNormalizer(unittest.TestCase):
    def test_windows_event_normalisation(self):
        raw_record = {
            "timestamp": "2026-11-06T08:00:00Z", 
            "source": "windows", 
            "event_id": 4625, 
            "username": "alex", 
            "source_ip": "192.0.2.25"
        }
        norm = normalise_record(raw_record, "windows")
        self.assertEqual(norm["event"]["provider"], "windows")
        self.assertEqual(norm["source"]["ip"], "192.0.2.25")
        self.assertEqual(norm["raw_reference"], raw_record)

    def test_firewall_event_normalisation(self):
        raw_record = {
            "ts": "2026-11-06T08:05:00Z", 
            "action": "blocked", 
            "id.orig_h": "198.51.100.20", 
            "id.resp_h": "192.0.2.10"
        }
        norm = normalise_record(raw_record, "firewall")
        self.assertEqual(norm["event"]["provider"], "firewall")
        self.assertEqual(norm["event"]["action"], "network_connection_blocked")
        self.assertEqual(norm["source"]["ip"], "198.51.100.20")
        self.assertEqual(norm["raw_reference"], raw_record)

if __name__ == "__main__":
    unittest.main()
