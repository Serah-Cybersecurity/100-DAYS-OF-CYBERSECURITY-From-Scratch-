from collections import Counter
from pathlib import Path
import re

# Locate the training data relative to this script dynamically.
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_FILE = SCRIPT_DIR.parent / "data" / "auth.log"

# Match usernames in standard OpenSSH-style messages:
# Failed password for USERNAME from IP ...
# Failed password for invalid user USERNAME from IP ...
FAILED_LOGIN_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from "
)
ACCEPTED_LOGIN_PATTERN = re.compile(
    r"Accepted password for (?:invalid user )?(\S+) from "
)

def load_log_lines(file_path):
    """Read a text log file line by line with robust error handling."""
    try:
        with file_path.open("r", encoding="utf-8") as file:
            return file.readlines()

    except FileNotFoundError:
        print(f"ERROR: Log file not found at: {file_path}")
        return None

    except PermissionError:
        print(f"ERROR: Permission denied when reading: {file_path}")
        return None

    except UnicodeDecodeError:
        print(f"ERROR: The file could not be decoded as UTF-8: {file_path}")
        return None

    except OSError as error:
        print(f"ERROR: Unable to read the log file: {error}")
        return None

def analyze_log_lines(lines):
    """Count selected authentication events and aggregate usernames."""
    failed_logins = 0
    accepted_logins = 0
    failed_users = Counter()
    malformed_lines = 0
    other_lines = 0

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Check for failed password patterns
        failed_match = FAILED_LOGIN_PATTERN.search(line)
        if failed_match:
            username = failed_match.group(1)
            failed_logins += 1
            failed_users[username] += 1
            continue

        # Check for accepted password patterns
        accepted_match = ACCEPTED_LOGIN_PATTERN.search(line)
        if accepted_match:
            accepted_logins += 1
            continue

        # Heuristic check for other recognized log message structures
        if re.match(
            r"^[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\S+\s+\S+:",
            line,
        ):
            other_lines += 1
        else:
            malformed_lines += 1

    return {
        "failed_logins": failed_logins,
        "accepted_logins": accepted_logins,
        "failed_users": failed_users,
        "malformed_lines": malformed_lines,
        "other_lines": other_lines,
    }

def print_report(results, total_lines):
    """Display a professional analysis report."""
    print("\n" + "=" * 50)
    print("LINUX AUTHENTICATION LOG ANALYSIS")
    print("=" * 50)

    print(f"Total input lines: {total_lines}")
    print(f"Failed-password messages: {results['failed_logins']}")
    print(f"Accepted-password messages: {results['accepted_logins']}")
    print(f"Other recognized-format messages: {results['other_lines']}")
    print(f"Malformed or unrecognized-format lines: {results['malformed_lines']}")

    print("\nFailed-password messages by username:")
    if results["failed_users"]:
        for username, count in results["failed_users"].most_common():
            print(f"  {username}: {count}")
    else:
        print("  No matching failed-password messages found.")

    print("\nINTERPRETATION AND LIMITATIONS")
    print("- Counts describe matching messages in this dataset.")
    print("- Repeated failures do not, by themselves, prove an active attack.")
    print("- Successful authentications do not prove all subsequent actions were authorized.")
    print("- The parser recognizes only a limited set of pre-defined message formats.")
    print("- This report does not establish identity, intent, or system compromise.")
    print("=" * 50)

def main():
    lines = load_log_lines(DATA_FILE)
    if lines is None:
        return

    results = analyze_log_lines(lines)
    print_report(results, len(lines))

if __name__ == "__main__":
    main()
