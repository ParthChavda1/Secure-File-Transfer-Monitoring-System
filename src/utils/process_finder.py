import psutil

def find_process_by_file_path(file_path):
    """
    Attempt to find which process is accessing a given file
    (Best-effort, NOT reliable)
    """
    for proc in psutil.process_iter(attrs=["pid", "name", "username"]):
        try:
            for f in proc.open_files():
                if f.path == file_path:
                    return {
                        "pid": proc.pid,
                        "process": proc.info["name"],
                        "user": proc.info["username"]
                    }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None
