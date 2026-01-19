import json
import time
from config.settings import ALERT_LOG
from src.utils.logger import get_json_logger

alert_logger = get_json_logger(ALERT_LOG)

def alert_admin(event_type,path,extra=None,severity="HIGH"):
    alert = {
        "event_type":event_type,
        "path": path,
        "extra": extra,
        "Severity": severity
    }
    alert_logger.warning(alert)
    print(f"[ALERT - {severity}] {event_type} → {path}")
    
