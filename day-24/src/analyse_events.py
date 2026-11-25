from collections import Counter
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "endpoint_events.jsonl"
REPORT_FILE = PROJECT_ROOT / "reports" / "endpoint_summary.json"
QUARANTINE_FILE = PROJECT_ROOT / "data" / "quarantine" / "invalid_events.jsonl"

REQUIRED_FIELDS = ("timestamp", "host", "channel", "event_id")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def _is_valid_iso_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        datetime.fromisoformat(normalized)
        return True
    except ValueError:
        return False


def validate_event(event: Any) -> str | None:
    """Return an error message if an event is invalid, or None if valid."""
    if not isinstance(event, dict):
        return "Event must be a JSON object"

    for field in REQUIRED_FIELDS:
        if field not in event or event[field] is None:
            return f"Missing required field: {field}"
        if isinstance(event[field], str) and not event[field].strip():
            return f"Empty required field: {field}"

    if not _is_valid_iso_timestamp(event["timestamp"]):
        return "Invalid timestamp format"

    event_id = event["event_id"]
    if isinstance(event_id, bool) or not isinstance(event_id, int):
        return "Invalid event_id: expected integer"

    return None


def analyse_events(input_path: Path) -> dict[str, Any]:
    valid_records = 0
    invalid_records: list[dict[str, Any]] = []
    event_counts: Counter[str] = Counter()
    successful_logons = 0
    failed_logons = 0

    with input_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            stripped = raw_line.strip()
            if not stripped:
                continue

            try:
                event = json.loads(stripped)
            except json.JSONDecodeError as exc:
                invalid_records.append({
                    "line": line_number,
                    "reason": f"Malformed JSON: {exc.msg}",
                    "raw_record": raw_line.rstrip("\r\n"),
                })
                continue

            error = validate_event(event)
            if error is not None:
                invalid_records.append({
                    "line": line_number,
                    "reason": error,
                    "raw_record": event,
                })
                continue

            valid_records += 1
            event_id = event["event_id"]
            event_counts[str(event_id)] += 1

            if event_id == 4624:
                successful_logons += 1
            elif event_id == 4625:
                failed_logons += 1

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_file": input_path.name,
        "total_valid_records": valid_records,
        "total_invalid_records": len(invalid_records),
        "event_id_counts": dict(event_counts),
        "successful_logons": successful_logons,
        "failed_logons": failed_logons,
        "invalid_records": invalid_records,
    }


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUARANTINE_FILE.parent.mkdir(parents=True, exist_ok=True)

    report = analyse_events(INPUT_FILE)
    REPORT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")

    with QUARANTINE_FILE.open("w", encoding="utf-8") as file:
        for record in report["invalid_records"]:
            file.write(json.dumps(record) + "\n")

    logging.info("Analysis complete")
    logging.info("Valid records: %s", report["total_valid_records"])
    logging.info("Invalid records: %s", report["total_invalid_records"])
    logging.info("Report: %s", REPORT_FILE)


if __name__ == "__main__":
    main()
