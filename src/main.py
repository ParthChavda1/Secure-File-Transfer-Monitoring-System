from src.config.sensitive import load_sensitive_paths
from src.monitor.file_watcher import start_monitoring
from src.utils.hash_store import load_hash_store, save_hash_store
from src.config.settings import MONITOR_PATHS
from src.monitor.baseline import build_baseline



if __name__ == "__main__":
    print("Environment Ready")
    print("Loaing Hash values...")
    load_hash_store()
    for path in MONITOR_PATHS:
        build_baseline(path)
    save_hash_store()
    load_sensitive_paths()
    start_monitoring()
