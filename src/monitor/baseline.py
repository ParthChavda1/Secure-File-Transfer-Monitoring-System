import os
from src.utils.hashing import calculate_hash
from src.utils.hash_store import update_hash
from src.utils.path_classifier import normalize_path

def build_baseline(directory):
    for root,_,files in os.walk(directory):
        for name in files:
            full_path = normalize_path(os.path.join(root,name))
            file_hash = calculate_hash(full_path)
            if(file_hash):
                update_hash(full_path,file_hash)