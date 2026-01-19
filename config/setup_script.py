import json
import os
from pathlib import Path

CONFIG_DIR = Path("config")
MONITOR_FILE = CONFIG_DIR / "monitor_paths.json"
SENSITIVE_FILE = CONFIG_DIR / "sensitive_paths.json"


def ensure_config_dir():
    CONFIG_DIR.mkdir(exist_ok=True)


def input_paths(prompt):
    print(prompt)
    print("Enter paths one by one. Type 'done' to finish.\n")

    paths = []
    while True:
        p = input("> ").strip()
        if p.lower() == "done":
            break

        if not os.path.exists(p):
            print(" Path does not exist. Try again.")
            continue

        paths.append(os.path.normpath(p))

    return list(set(paths))


def write_json(path, data):
    
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def main():
    print("\n---------- Secure File Transfer Monitor – One-Time Setup ----------\n")

    ensure_config_dir()

    monitor_dirs = input_paths(
        "Enter directories to MONITOR (watchdog will observe these):"
    )

    sensitive_dirs = input_paths(
        "Enter SENSITIVE directories (alerts will be raised):"
    )

    sensitive_files = input_paths(
        "Enter SENSITIVE files (full path):"
    )

    write_json(MONITOR_FILE, {"directories": monitor_dirs})
    write_json(
        SENSITIVE_FILE,
        {
            "directories": sensitive_dirs,
            "files": sensitive_files
        }
    )

    print("\n Setup complete.")
    print("Configuration saved in /config")
    print("You can now run the monitoring agent.\n")


if __name__ == "__main__":
    main()
