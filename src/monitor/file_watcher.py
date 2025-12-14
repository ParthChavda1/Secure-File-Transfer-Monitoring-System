import time
from watchdog.observers import Observer
from src.monitor.event_handler import FileEventHandler
from src.config.settings import MONITOR_PATHS

def start_monitoring():
    event_handler = FileEventHandler()
    observer = Observer()

    for path in MONITOR_PATHS:
        observer.schedule(event_handler,path,recursive=True)
        print(f"Monitoring Started on: {path}")
    
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()