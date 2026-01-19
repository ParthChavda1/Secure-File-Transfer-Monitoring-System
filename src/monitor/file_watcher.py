import time
import json
from watchdog.observers import Observer
from src.monitor.event_handler import FileEventHandler



def start_monitoring():
    with open("config/monitor_paths.json","r") as f:
        MONITOR_PATHS = json.load(f) 
    event_handler = FileEventHandler()
    observer = Observer()

    for path in MONITOR_PATHS["directories"]:
        observer.schedule(event_handler,path,recursive=True)
        print(f"Monitoring Started on: {path}")
    
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()