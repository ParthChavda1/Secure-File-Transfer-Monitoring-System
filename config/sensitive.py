import json
import os

from src.utils.alert import alert_admin
from src.utils.hash_store import get_hash
from src.utils.hashing import calculate_hash
from src.utils.path_classifier import normalize_path

_sensitive_dirs =  set()
_sensitive_files =  set()
_SENSITIVE_JSON = "config\sensitive_paths.json"


def load_sensitive_paths(file_path = _SENSITIVE_JSON):
    global _sensitive_dirs,_sensitive_files
    
    with open(file_path,"r") as f:
        data = json.load(f)
    
    _sensitive_dirs = {
        normalize_path(p) for p in data.get("directories",[])
    }
    _sensitive_files = {
        normalize_path(p) for p in data.get("files",[])
    }
    

def reconcile_sensitive_files():
    for f in list(_sensitive_files):
        if not os.path.exists(f):
            alert_admin(
                "SENSITIVE_FILE_MISSING_OR_RENAMED",
                f,
                severity="HIGH"
            )
            continue
        
        old_hash = get_hash(f)
        if not old_hash:
            continue
        
        current_hash = calculate_hash(f)
        if current_hash != old_hash:
            alert_admin(
                "OFFLINE_INTEGRITY_VIOLATION",
                f,
                extra={
                    "expected_hash": old_hash,
                    "current_hash": current_hash
                },
                severity="CRITICAL"
            )

            


def is_sensitive(path):
    path = normalize_path(path)
    if path in _sensitive_files :
        return True
    for sensitive_dir in _sensitive_dirs:
        if path.startswith(sensitive_dir + os.sep):
            return True
    return False

def update_sensitive_json(old_path,new_path):
    with open(_SENSITIVE_JSON,"r") as f:
        data = json.loads(f)
    
    data["files"] = list(_sensitive_files)
    
    with open(_SENSITIVE_JSON, "w") as f:
            json.dump(data, f, indent=4)
     

def propagate_sensitive_rename(old_path, new_path):
    old_path = normalize_path(old_path)
    new_path = normalize_path(new_path)

    if old_path in _sensitive_files:
        _sensitive_files.remove(old_path)
        _sensitive_files.add(new_path)
        
        update_sensitive_json(old_path,new_path)
        return True

    for d in _sensitive_dirs:
        if old_path.startswith(d + os.sep):
            return True

    return False

