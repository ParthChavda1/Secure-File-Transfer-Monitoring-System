import json
from config.sensitive import load_sensitive_paths,reconcile_sensitive_files
from src.monitor.file_watcher import start_monitoring
from src.utils.hash_store import load_hash_store, save_hash_store
from src.monitor.baseline import build_baseline



if __name__ == "__main__":
    print("Environment Ready")
    print("Loaing Hash values...")
    load_hash_store()
    load_sensitive_paths()
    reconcile_sensitive_files()
    with open("config/monitor_paths.json","r") as f:
        MONITOR_PATHS = json.load(f) 
    
    for path in MONITOR_PATHS["directories"]:
        build_baseline(path)
    save_hash_store()
    start_monitoring()
