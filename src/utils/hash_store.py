import json
import os
from config.settings import HASH_STORE_FILE

_hash_store = {}

def load_hash_store():
    global _hash_store
    if os.path.exists(HASH_STORE_FILE):
        with open(HASH_STORE_FILE,"r") as f:
            _hash_store = json.load(f)
    else:
        _hash_store ={}
    
def save_hash_store():
    with open(HASH_STORE_FILE,"w") as f:
        json.dump(_hash_store,f,indent=2)
        
def update_hash(path,file_hash):
    _hash_store[path] = file_hash
    save_hash_store()
    
def remove_hash(path):
    old_hash = _hash_store.pop(path,None)
    save_hash_store()
    return old_hash

def get_hash(path):
    return _hash_store.get(path)