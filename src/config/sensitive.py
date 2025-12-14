import json
import os

from src.utils.path_classifier import normalize_path

_sensitive_dirs =  set()
_sensitive_files =  set()


def load_sensitive_paths(file_path = "src\config\sensitive_paths.json"):
    global _sensitive_dirs,_sensitive_files
    
    with open(file_path,"r") as f:
        data = json.load(f)
    
    _sensitive_dirs = {
        normalize_path(p) for p in data.get("directories",[])
    }
    _sensitive_files = {
        normalize_path(p) for p in data.get("files",[])
    }
    
    
def is_sensitive(path):
    path = normalize_path(path)
    if path in _sensitive_files:
        return True
    return any(path.startswith(d) for d in _sensitive_dirs)