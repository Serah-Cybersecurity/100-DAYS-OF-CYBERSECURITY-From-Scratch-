import json
from pathlib import Path
import yaml

RULES_DIR = Path("rules/windows")
FIXTURE_FILE = Path("tests/fixtures/windows_events.jsonl")


def load_rules(rules_dir: Path):
    rules = []
    for rule_path in sorted(rules_dir.glob("*.yml")):
        with rule_path.open("r", encoding="utf-8") as f:
            rule_data = yaml.safe_load(f)
        event_ids = rule_data["detection"]["selection"]["EventID"]
        if not isinstance(event_ids, list):
            event_ids = [event_ids]
        rules.append({
            "file": rule_path.name,
            "title": rule_data["title"],
            "event_ids": set(event_ids),
        })
    return rules


def load_events(fixture_file: Path):
    events = []
    with fixture_file.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events


def main():
    rules = load_rules(RULES_DIR)
    events = load_events(FIXTURE_FILE)

    for rule in rules:
        matched = [ev for ev in events if ev.get("EventID") in rule["event_ids"]]
        print(f"\nRule File: {rule['file']} ({rule['title']})")
        print(f"Rule EventIDs: {sorted(rule['event_ids'])}")
        print(f"Match Count: {len(matched)}")
        for ev in matched:
            print(f"  - EventID={ev['EventID']} Account={ev['AccountName']} Computer={ev['Computer']}")


if __name__ == "__main__":
    main()
