import json
import os
from backend.config import OUTPUT_DIR

def report_step(step, status, error=None):
    record = {
        "description": step.get("raw"),
        "action": step.get("action"),
        "status": status,
        "error": error
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "report.json")

    if os.path.exists(path):
        data = json.load(open(path))
    else:
        data = []

    data.append(record)
    json.dump(data, open(path, "w"), indent=2)
