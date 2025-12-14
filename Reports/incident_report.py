import json
from collections import Counter, defaultdict
from pathlib import Path

ALERT_LOG = Path("logs/alerts.log")


def load_alerts():
    alerts = []
    if not ALERT_LOG.exists():
        print("No alert log found.")
        return alerts

    with open(ALERT_LOG, "r") as f:
        for line in f:
            try:
                record = json.loads(line)
                event = record.get("event", {})
                alerts.append({
                    "timestamp": record.get("timestamp"),
                    "level": record.get("level"),
                    "event_type": event.get("event_type"),
                    "path": event.get("path"),
                    "severity": event.get("Severity"),
                    "extra": event.get("extra")
                })
            except json.JSONDecodeError:
                continue
    return alerts


def main():
    alerts = load_alerts()

    print("\n---------- Incident Summary Report ----------n")
    print(f"Total Incidents Detected: {len(alerts)}\n")

    if not alerts:
        return

    # Severity breakdown
    severity_count = Counter(a["severity"] for a in alerts)
    print("Severity Breakdown:")
    for sev, count in severity_count.items():
        print(f"  {sev}: {count}")

    # Event type breakdown
    event_type_count = Counter(a["event_type"] for a in alerts)
    print("\nViolation Types:")
    for etype, count in event_type_count.items():
        print(f"  {etype}: {count}")

    # Top affected files
    file_count = Counter(a["path"] for a in alerts)
    print("\nMost Affected Files:")
    for path, count in file_count.most_common(5):
        print(f"  {path} ({count} incidents)")

    # Critical incidents detailed view
    print("\n---------- CRITICAL INCIDENTS ----------")
    criticals = [a for a in alerts if a["severity"] == "CRITICAL"]

    if not criticals:
        print("  None")
    else:
        for inc in criticals:
            print(
                f"- [{inc['timestamp']}] "
                f"{inc['event_type']} → {inc['path']}"
            )

    print("\n---------- End of Report ----------\n")


if __name__ == "__main__":
    main()
