import json
import datetime

log_file = 'actions_log.json'

def log_action(module, action):
    log_entry = {
        "module": module,
        "action": action,
        "timestamp": datetime.datetime.now().isoformat()
    }
    try:
        with open(log_file, 'r') as file:
            logs = json.load(file)
    except FileNotFoundError:
        logs = []

    logs.append(log_entry)
    
    # Debug: Print log entry being added
    print(f"Adding log entry: {log_entry}")

    with open(log_file, 'w') as file:
        json.dump(logs, file, indent=4)
        # Debug: Confirm writing to file
        print(f"Written to {log_file}: {logs}")
