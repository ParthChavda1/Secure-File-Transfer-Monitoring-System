import json
from datetime import date
from collections import Counter
from pathlib import Path

ACTIVITY_LOG  = Path("logs/activity.log")

def load_events():
    events = []
    if not ACTIVITY_LOG.exists():
        print("No Activity Log Found")
        return events
    with open(ACTIVITY_LOG,"r") as f:
        for line in f:
            try:
                data = json.loads(line)
                
                if data.get("timestamp").split(" ")[0] == (str)(date.today()):
                    events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
                
    return events

def main():
    events = load_events()
    print("---------Daily Activity Report---------")
    
    print(f"Total Events: {len(events)}")
    event_counts = Counter(e.get("event").get("event_type") for e in events)
    for event, count in event_counts.items():
        print(f"{event}: {count}")
        
    print("\n Top Modified Files:")
    modified = (e.get("event")["file"] for e in events if e.get("event").get("event_type") == "MODIFIED")
    # for path in modified:
    #     print(path)
    for path,count in Counter(modified).items():
        print(f"- {path} ({count} times)")

    
    
    

if __name__ == "__main__":
    main()