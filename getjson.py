import json

def get_json():
    with open('log.json') as f:
        data = json.load(f)
        return data

def update_json(data):
    with open("log.json", "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)
