import json
from pathlib import Path

DATA_FILE = Path("tests/fixtures/windows_events.jsonl")


def load_events():
    events = []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                events.append(json.loads(line))
    return events


def failed_logon_rule(event):
    return event.get("EventID") == 4625


def account_lockout_rule(event):
    return event.get("EventID") == 4740


def authentication_events_rule(event):
    return event.get("EventID") in (4624, 4625)


def main():
    events = load_events()
    tests = {
        "failed_logon": failed_logon_rule,
        "account_lockout": account_lockout_rule,
        "authentication_events": authentication_events_rule,
    }

    for rule_name, rule_function in tests.items():
        matches = [
            event
            for event in events
            if rule_function(event)
        ]
        print(f"\nRule: {rule_name}")
        print(f"Matches: {len(matches)}")
        for event in matches:
            print(
                event["EventID"],
                event["AccountName"],
                event["Computer"]
            )


if __name__ == "__main__":
    main()
