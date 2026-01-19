import subprocess
import json
import time


def query_security_events(lookback_seconds=20):

    ps_cmd = f"""
    $start = (Get-Date).AddSeconds(-{lookback_seconds})
    Get-WinEvent -FilterHashtable @{{
        LogName='Security';
        StartTime=$start
    }} | Where-Object {{ $_.Id -in 4663,4660 }} | Select-Object TimeCreated, Id, Message, Properties | ConvertTo-Json
    """

    result = subprocess.run(
        ["powershell", "-Command", 
         ps_cmd
         ],
        capture_output=True,
        text=True,
        # run_as_admin = True
    )

    if not result.stdout.strip():
        return []

    try:
        data = json.loads(result.stdout)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return []
