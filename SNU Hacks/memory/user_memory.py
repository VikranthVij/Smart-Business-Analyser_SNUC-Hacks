import json
import os

FILE = "memory/user_profiles.json"

def load_profiles():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_profiles(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user_profile(user_id):
    data = load_profiles()
    return data.get(user_id, {})

def update_user_profile(user_id, new_data):
    data = load_profiles()
    
    if user_id not in data:
        data[user_id] = {}

    data[user_id].update(new_data)
    save_profiles(data)