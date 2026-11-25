import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "endpoint_events.jsonl"
DEFAULT_REPORT_FILE = PROJECT_ROOT / "reports" / "endpoint_summary.json"
DEFAULT_QUARANTINE_FILE = PROJECT_ROOT / "data" / "quarantine" / "invalid_events.jsonl"

REQUIRED_FIELDS = ("timestamp", "host", "channel", "event_id")
LOGON_EVENT_IDS = {4624, 4625}
PROCESS_NETWORK_EVENT_IDS = {1, 3, 4688}
AUDIT_CLEARED_EVENT_ID = 1102

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def parse_iso_timestamp(value: Any) -> datetime | None:
    """Parse an ISO-8601 timestamp into a timezone-aware datetime, or None."""
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _is_valid_iso_timestamp(value: Any) -> bool:
    return parse_iso_timestamp(value) is not None


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


def _slim_event_for_timeline(event: dict[str, Any]) -> dict[str, Any]:
    """Keep core and contextual fields present on the event without fabricating values."""
    optional_keys = (
        "username",
        "source_ip",
        "process_name",
        "parent_process",
        "destination_ip",
        "message",
    )
    entry: dict[str, Any] = {
        "timestamp": event["timestamp"],
        "host": event["host"],
        "channel": event["channel"],
        "event_id": event["event_id"],
    }
    for key in optional_keys:
        if key in event and event[key] is not None:
            entry[key] = event[key]
    return entry


def analyse_events(input_path: Path) -> dict[str, Any]:
    valid_entries: list[tuple[datetime, int, dict[str, Any]]] = []
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

            parsed_dt = parse_iso_timestamp(event["timestamp"])
            assert parsed_dt is not None

            event_id = event["event_id"]
            event_counts[str(event_id)] += 1

            if event_id == 4624:
                successful_logons += 1
            elif event_id == 4625:
                failed_logons += 1

            valid_entries.append((parsed_dt, line_number, _slim_event_for_timeline(event)))

    valid_entries.sort(key=lambda item: (item[0], item[1]))
    timeline = [item[2] for item in valid_entries]
    logon_sequence = [ev for ev in timeline if ev["event_id"] in LOGON_EVENT_IDS]
    process_and_network_events = [
        ev for ev in timeline if ev["event_id"] in PROCESS_NETWORK_EVENT_IDS
    ]
    audit_log_cleared_events = [
        ev for ev in timeline if ev["event_id"] == AUDIT_CLEARED_EVENT_ID
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_file": input_path.name,
        "total_valid_records": len(timeline),
        "total_invalid_records": len(invalid_records),
        "event_id_counts": dict(event_counts),
        "successful_logons": successful_logons,
        "failed_logons": failed_logons,
        "timeline": timeline,
        "logon_sequence": logon_sequence,
        "process_and_network_events": process_and_network_events,
        "audit_log_cleared_events": audit_log_cleared_events,
        "invalid_records": invalid_records,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate, sort, and summarize JSONL endpoint telemetry."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_FILE,
        help="Path to input JSONL event file",
    )
    parser.add_argument(
        "--output-report",
        type=Path,
        default=DEFAULT_REPORT_FILE,
        help="Path to output JSON summary report",
    )
    parser.add_argument(
        "--quarantine-file",
        type=Path,
        default=DEFAULT_QUARANTINE_FILE,
        help="Path to output JSONL file for invalid/malformed records",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_arg_parser().parse_args(argv)
    input_path: Path = args.input
    report_path: Path = args.output_report
    quarantine_path: Path = args.quarantine_file

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    quarantine_path.parent.mkdir(parents=True, exist_ok=True)

    report = analyse_events(input_path)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    with quarantine_path.open("w", encoding="utf-8") as file:
        for record in report["invalid_records"]:
            file.write(json.dumps(record) + "\n")

    logging.info("Analysis complete")
    logging.info("Valid records: %s", report["total_valid_records"])
    logging.info("Invalid records: %s", report["total_invalid_records"])
    logging.info("Report: %s", report_path)


if __name__ == "__main__":
    main()
