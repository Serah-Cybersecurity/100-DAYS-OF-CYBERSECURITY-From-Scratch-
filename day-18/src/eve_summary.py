import json
import sys

from collections import Counter
from pathlib import Path


def analyse_eve_file(path: Path):
    """
    Read Suricata EVE JSON and summarise event types and alerts.

    EVE is newline-delimited JSON:
    one JSON object per line.
    """

    event_counts = Counter()
    signature_counts = Counter()
    severity_counts = Counter()

    total_records = 0
    malformed_records = 0
    alert_count = 0

    if not path.exists():
        raise FileNotFoundError(
            f"Input file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(file, start=1):

            line = line.strip()

            if not line:
                continue

            try:
                event = json.loads(line)

            except json.JSONDecodeError:
                malformed_records += 1

                print(
                    f"Warning: malformed JSON at line {line_number}",
                    file=sys.stderr
                )

                continue

            if not isinstance(event, dict):
                malformed_records += 1
                continue

            total_records += 1

            event_type = event.get(
                "event_type",
                "unknown"
            )

            event_counts[event_type] += 1

            if event_type == "alert":

                alert_count += 1

                alert = event.get("alert") or {}

                signature = alert.get(
                    "signature",
                    "Unknown signature"
                )

                severity = alert.get(
                    "severity",
                    "Not supplied"
                )

                signature_counts[signature] += 1
                severity_counts[str(severity)] += 1

    return {
        "total_records": total_records,
        "malformed_records": malformed_records,
        "alert_count": alert_count,
        "event_counts": event_counts,
        "signature_counts": signature_counts,
        "severity_counts": severity_counts,
    }


def main():

    input_path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("output/suricata/eve.json")
    )

    try:
        results = analyse_eve_file(input_path)

    except (OSError, ValueError) as error:

        print(
            f"Error: {error}",
            file=sys.stderr
        )

        raise SystemExit(1)

    print("\nSURICATA EVE ANALYSIS")
    print("=" * 35)

    print(
        f"Records analysed: "
        f"{results['total_records']}"
    )

    print(
        f"Alerts: "
        f"{results['alert_count']}"
    )

    print(
        f"Malformed records: "
        f"{results['malformed_records']}"
    )

    print("\nEVENT TYPES")

    for event_type, count in sorted(
        results["event_counts"].items()
    ):

        print(f"{event_type}: {count}")

    print("\nALERT SIGNATURES")

    if not results["signature_counts"]:

        print("No alert records found.")

    else:

        for signature, count in (
            results["signature_counts"].most_common()
        ):

            print(f"{signature}: {count}")

    print("\nALERT SEVERITY")

    if not results["severity_counts"]:

        print("No severity information available.")

    else:

        for severity, count in sorted(
            results["severity_counts"].items()
        ):

            print(f"{severity}: {count}")

    print(
        "\nNOTE: This tool summarises logged events. "
        "It does not determine whether activity is malicious."
    )


if __name__ == "__main__":
    main()
