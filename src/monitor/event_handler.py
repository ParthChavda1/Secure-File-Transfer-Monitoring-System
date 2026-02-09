import os
import time
from watchdog.events import FileSystemEventHandler
from src.utils.alert import alert_admin
from src.utils.hash_store import get_hash, remove_hash, update_hash
from src.utils.logger import get_json_logger
from config.settings import LOG_DIR
from src.utils.hashing import calculate_hash
from config.sensitive import is_sensitive
from src.utils.path_classifier import normalize_path
from src.utils.user_attribution import get_actor
from config.sensitive import is_sensitive,propagate_sensitive_rename


activity_logger = get_json_logger(LOG_DIR)

def classify_move(old_path, new_path):
    old_dir = os.path.dirname(old_path)
    new_dir = os.path.dirname(new_path)

    if old_dir == new_dir:
        return "RENAME"
    return "MOVE"
    
class FileEventHandler(FileSystemEventHandler):   
    
    def log_event(self,event_type,path,extra=None,sensitive=False):
        log_entry={
            "event_type":event_type,
            "file":path,
            "extra": extra,
        }
        if(sensitive):
            activity_logger.warning(log_entry)
        else:
            activity_logger.info(log_entry)



    def on_created(self, event):
        if not event.is_directory:
            # activity_logger.info(f"[Created] {event.src_path}")
            path = normalize_path(event.src_path)
            file_hash = calculate_hash(path)
            if is_sensitive(path):
                alert_admin(
                    "FILE CREATED IN SENSITIVE DIRECTORY",
                    path,
                )
            update_hash(path,file_hash)
            self.log_event("CREATED",path,extra = {"hash": file_hash})
    
    def on_modified(self,event):
        
        if not event.is_directory:
            # activity_logger.info(f"[Modified] {event.src_path}")
            path = normalize_path(event.src_path)
            
            old_hash = get_hash(path)
            new_hash = calculate_hash(path)
            if old_hash and new_hash and old_hash != new_hash:
                self.log_event("INTEGRETY VIOLATION",path,extra={"old_hash":old_hash,"new_hash":new_hash})
            update_hash(path,new_hash)
            if is_sensitive(path):
                alert_admin("SENSITIVE FILE MODIFIED",path)
                self.log_event("MODIFIED",path,extra = {"hash":new_hash},sensitive=True)
            else:
                self.log_event("MODIFIED",path,extra = {"hash":new_hash})
        
    def on_moved(self, event):
        if not event.is_directory: 
            # activity_logger.info(f"[MOVED] {event.src_path} -> {event.dest_path}")
            new_path = normalize_path(event.dest_path)
            old_path = normalize_path(event.src_path)
            action =classify_move(old_path,new_path)
            was_sensitive = is_sensitive(old_path)
            if was_sensitive:
                propagate_sensitive_rename(old_path,new_path)
            file_hash = remove_hash(old_path)
            if file_hash:
                update_hash(new_path,file_hash)
            
            if was_sensitive:
                if action == "RENAME":
                    alert_admin(
                        "SENSITIVE FILE RENAMED",
                        old_path,
                        extra={"new_name": os.path.basename(new_path)}
                    )
                else:
                    alert_admin(
                    "SENSITIVE_FILE_MOVED",
                    old_path,
                    extra={"new_path": new_path}
                )
            
            self.log_event(
                action,
                old_path,
                extra={"new_path": new_path, "hash": file_hash},
                sensitive=was_sensitive
            )
            
    def on_deleted(self, event):
        if not event.is_directory:
            # activity_logger.info(f"[DELETED] {event.src_path}")
            path = normalize_path(event.src_path)

            old_hash = remove_hash(path)
            if is_sensitive(path):
                alert_admin("SENSITIVE FILE DELETED",path)
                self.log_event("DELETED",path,extra={"last_known_hash":old_hash},sensitive=True)
            else:
                self.log_event("DELETED",path,extra={"last_known_hash":old_hash})


