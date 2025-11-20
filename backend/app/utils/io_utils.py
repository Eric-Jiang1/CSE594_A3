import json

def load_json(path: str):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_json(path: str, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
