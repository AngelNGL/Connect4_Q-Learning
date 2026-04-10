import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_DIR = BASE_DIR/"Data"
SETTINGS_FILE = str(SETTINGS_DIR/"settings.json")
DEFAULT_EPSILON = 0.1


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"epsilon": DEFAULT_EPSILON}

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        epsilon = float(data.get("epsilon", DEFAULT_EPSILON))
        if 0.0 <= epsilon <= 1.0:
            return {"epsilon": epsilon}
    except (ValueError, TypeError, json.JSONDecodeError):
        pass

    return {"epsilon": DEFAULT_EPSILON}

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=2)

def get_epsilon():
    return load_settings()["epsilon"]

def set_epsilon(value):
    save_settings({"epsilon": value})
