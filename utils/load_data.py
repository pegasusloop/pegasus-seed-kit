import json
import os

def load_substack_data():
    path = os.path.join("data", "substack.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
