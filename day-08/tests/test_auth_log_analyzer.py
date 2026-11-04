import sys
import unittest
from pathlib import Path

# Locate project directory and add 'python' folder to system path
PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR / "python"))

from auth_log_analyzer import analyze_log_lines

class TestAuthLogAnalyzer(unittest.TestCase):

    def test_failed_login_count(self):
        """Test that failed and accepted logins are counted correctly."""
        lines = [
            "Oct 27 09:01:02 parrot sshd[1001]: Failed password for test_user from 192.0.2.15 port 51001 ssh2",
            "Oct 27 09:02:10 parrot sshd[1002]: Accepted password for demo_user from 198.51.100.25 port 52001 ssh2",
        ]
        results = analyze_log_lines(lines)
        self.assertEqual(results["failed_logins"], 1)
        self.assertEqual(results["accepted_logins"], 1)

    def test_failed_logins_by_username(self):
        """Test that failed login counts are tracked accurately per username."""
        lines = [
            "Oct 27 09:01:02 parrot sshd[1001]: Failed password for test_user from 192.0.2.15 port 51001 ssh2",
            "Oct 27 09:01:14 parrot sshd[1002]: Failed password for test_user from 192.0.2.15 port 51002 ssh2",
            "Oct 27 09:04:30 parrot sshd[1003]: Failed password for invalid user unknown_user from 203.0.113.40 port 53001 ssh2",
        ]
        results = analyze_log_lines(lines)
        self.assertEqual(results["failed_users"]["test_user"], 2)
        self.assertEqual(results["failed_users"]["unknown_user"], 1)

    def test_malformed_line_is_counted(self):
        """Test that malformed lines are captured and counted properly."""
        lines = [
            "This is an intentionally malformed training record."
        ]
        results = analyze_log_lines(lines)
        self.assertEqual(results["malformed_lines"], 1)
        self.assertEqual(results["failed_logins"], 0)

    def test_empty_input(self):
        """Test that an empty list of lines handles gracefully without crashing."""
        results = analyze_log_lines([])
        self.assertEqual(results["failed_logins"], 0)
        self.assertEqual(results["accepted_logins"], 0)
        self.assertEqual(results["malformed_lines"], 0)

if __name__ == "__main__":
    unittest.main()
