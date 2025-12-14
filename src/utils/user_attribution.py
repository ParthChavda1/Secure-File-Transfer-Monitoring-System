import subprocess

from src.utils.path_classifier import normalize_path
from src.utils.security_log_reader import query_security_events


def sid_to_username(sid):
    ps_cmd = f"""
    try {{
        (New-Object System.Security.Principal.SecurityIdentifier("{sid}"))
        .Translate([System.Security.Principal.NTAccount]).Value
    }} catch {{
        "UNKNOWN"
    }}
    """

    result = subprocess.run(
        ["powershell", "-Command", ps_cmd],
        capture_output=True,
        text=True
    )

    return result.stdout.strip() if result.stdout.strip() else "UNKNOWN"


def extract_sid(event):
    try:
        return event["Properties"][1]["Value"]
    except Exception:
        return None

def get_actor(path, event_time, lookback_seconds=20):
    """
    Attempts to attribute a filesystem event to a user
    using Windows Security logs.
    """

    # path = normalize_path(path)
    events = query_security_events(lookback_seconds)

    for event in events:
        message = normalize_path(event.get("Message", ""))
        if path.lower() in message.lower():
            sid = extract_sid(event)
            if sid:
                return sid_to_username(sid)

    return "UNKNOWN"