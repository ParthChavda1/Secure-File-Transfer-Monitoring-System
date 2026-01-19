# Secure File Monitoring Agent (Windows)

## Overview

Secure File Monitoring Agent is a Windows host-based security tool designed to detect, log, and alert on unauthorized modifications and deletions of sensitive files and directories. The system operates as a **non-interactive monitoring agent**, using policy-driven rules defined during a one-time administrative setup.

The agent continuously monitors configured directories for file system events, evaluates them against sensitivity policies, and generates structured logs and alerts for high-risk activity. The design mirrors real-world endpoint security and file integrity monitoring (FIM) systems.

User attribution via Windows Security Event Logs is planned as a future enhancement. Until then, unattributed sensitive actions are explicitly flagged with elevated severity.

---

## Key Features

- Real-time file system monitoring using Watchdog
- Policy-based classification of sensitive files and directories
- Severity-based alert generation (`HIGH`, `CRITICAL`)
- Structured JSON logging for activities and alerts
- Baseline hashing and integrity tracking
- Offline reporting scripts for security review
- Modular, extensible architecture

---

## Project Structure
```
SecureFileMonitor/
│
├── config/
│ ├── monitor_paths.json
│ ├── sensitive_paths.json
│ ├── sensitive.py
│ ├── settings.py
│ ├── setup_script.py
│
├── src/
│ ├── monitor/
│ │ ├── baseline.py
│ │ ├── event_handler.py
│ │ ├── file_watcher.py
│ │
│ ├── utils/
│ │ ├── alert.py
│ │ ├── hash_store.py
│ │ ├── hashing.py
│ │ ├── logger.py
│ │ ├── path_classifier.py
│ │ ├── security_log_reader.py
│ │ ├── user_attribution.py
│
│ ├── main.py
│
├── Reports/
│ ├── daily_activity_report.py
│ ├── incident_report.py
│
├── logs/
├── hash_store.json # runtime state (ignored in git)
├── requirements.txt
├── README.md
├── .gitignore

```

---



## Installation

### Clone the repository

```bash
git clone https://github.com/ParthChavda1/Secure-File-Transfer-Monitoring-System
````

### Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

* * *

## One-Time Administrative Setup

Before running the agent, an administrator must define:

- Directories to monitor
- Sensitive directories and files

These policies are stored in JSON configuration files:

### Running the Setup Script

Run this script **once** to setup directories to monitor, sensitive directories and files:

```bash
python config/setup_script.py
```

Running the Agent
-----------------

After configuration, start the monitoring agent:

```bash
python main.py
```

*   Activity logs are written to `logs/activity.log`
*   Alerts are written to `logs/alerts.log`

* * *

Logging and Alerts
------------------

*   All file system events are logged in **structured JSON format**
*   Sensitive file modifications and deletions trigger alerts
*   Unattributed sensitive actions are marked as **CRITICAL**
*   Logs are intended for **audit and incident analysis**, not real-time UI display

* * *

Reporting
---------

Offline reports can be generated from stored logs:

```bash
python Reports/daily_activity_report.py
python Reports/incident_report.py
```

### Reports summarize:

*   Sensitive file activity
*   Alert frequency
*   High-risk incidents requiring investigation

* * *



Limitations
-----------

*   Windows-only implementation
*   High-frequency file activity may cause delayed processing
*   No real-time notification (email/SIEM integration not implemented)

* * *

