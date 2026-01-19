SecureFileMonitor/
│
├── src/
│   ├── monitor/
│   │   ├── file_watcher.py
│   │   ├── event_handler.py
│   │
│   ├── utils/
│   │   ├── hashing.py
│   │   ├── logger.py
│   │   ├── path_classifier.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── sensitive_paths.json
│   │
│   ├── main.py
│
├── logs/
│   ├── activity.log
│   ├── alerts.log
│
├── reports/
│
├── venv/  (auto-created)
│
├── requirements.txt
│
└── README.md


# Secure File Monitoring Agent

## Project Overview

Secure File Monitoring Agent is a Windows host-based tool designed to monitor, log, and alert on unauthorized modifications, deletions, or moves of sensitive files and directories. The agent is non-interactive and policy-driven, running silently after a one-time administrative setup.

The system uses:

- **Policy files** to define directories to monitor and sensitive files/folders.
- **Watchdog** to detect file system events in real time.
- **Alerting engine** to classify sensitive actions by severity.
- **Structured logging** for activity and security incidents.
- **Offline reporting scripts** for audit and incident review.

User attribution (authentication) is planned to be implemented using Windows Security Event Logs to map actions to responsible users. Currently, unattributed actions are flagged as `UNKNOWN` with high severity.

---

## Features

- Real-time monitoring of configured directories.
- Policy-driven detection of sensitive files and folders.
- Event logging in structured JSON format.
- Severity-based alert generation (`HIGH` / `CRITICAL`).
- Offline reporting scripts:
  - `daily_activity_report.py`
  - `incident_report.py`
- Modular architecture separating configuration, monitoring, alerting, and reporting.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/secure-file-monitoring-agent.git
