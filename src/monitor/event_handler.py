from watchdog.events import FileSystemEventHandler
import time
from src.utils.alert import alert_admin
from src.utils.hash_store import remove_hash, update_hash
from src.utils.logger import get_json_logger
from src.config.settings import LOG_DIR
from src.utils.hashing import calculate_hash
from src.config.sensitive import is_sensitive
from src.utils.path_classifier import normalize_path
from src.utils.user_attribution import get_actor



activity_logger = get_json_logger(LOG_DIR)
    
class FileEventHandler(FileSystemEventHandler):   
    
    def log_event(self,event_type,path,extra=None,sensitive=False):
        user = get_actor(path,time.time())

        if user == "UNKNOWN":
            alert_admin(
                event_type="SENSITIVE_FILE_ACTION_UNATTRIBUTED",
                path=path,
                severity="CRITICAL"
            )
        else:
            alert_admin(
                event_type="SENSITIVE_FILE_ACTION",
                path=path,
                extra={"user": user},
                severity="HIGH"
            )
        log_entry={
            "event_type":event_type,
            "file":path,
            "user":user,
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
            update_hash(path,file_hash)
            self.log_event("CREATED",path,extra = {"hash": file_hash})
    
    def on_modified(self,event):
        
        if not event.is_directory:
            # activity_logger.info(f"[Modified] {event.src_path}")
            path = normalize_path(event.src_path)
            
            new_hash = calculate_hash(path)
            old_hash = calculate_hash(path)
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
            src_sensitive = is_sensitive(old_path)
            dest_sensitive = is_sensitive(new_path)
            if src_sensitive and not dest_sensitive:
                alert_admin("SENSITIVE FILE MOVED OUT",old_path,extra = {"dest":new_path})
            elif not src_sensitive and dest_sensitive:
                alert_admin("SENSITIVE FILE MOVED IN",new_path)
            file_hash = remove_hash(old_path)
            if file_hash:
                update_hash(new_path,file_hash)
            if src_sensitive ^ dest_sensitive:
                self.log_event("MOVED",old_path,extra={"new_path":new_path,"hash":file_hash},sensitive=True)
            else:    
                self.log_event("MOVED",old_path,extra={"new_path":new_path,"hash":file_hash})
            
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


