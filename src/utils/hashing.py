import hashlib

import hashlib
import time


def calculate_hash(file_path, retries=3, delay=0.5):
    for _ in range(retries):
        try:
            sha256 = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except PermissionError:
            time.sleep(delay)

    # If still not readable
    return None
