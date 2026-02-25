import json
import os
import subprocess
import time
from pynput import keyboard
from dotenv import load_dotenv

load_dotenv()

CHROME_PATH = os.getenv("CHROME_PATH")
VS_PATH = os.getenv("VS_PATH")

def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

def validate_path():
    if not CHROME_PATH or not os.path.exists(CHROME_PATH):
        raise FileNotFoundError("Chrome path invalid")
    if not VS_PATH or not os.path.exists(VS_PATH):
        raise FileNotFoundError("Visual studio path invalid")
    
def launch_application():
    config = load_config()
    subprocess.Popen([CHROME_PATH, config['url']])
    time.sleep(config['launch_delay'])
    subprocess.Popen([VS_PATH])

def format_hotkey(keys):
    special_keys = {"ctrl", "alt", "shift", "enter", "tab", "esc"}

    formatted = []
    for key in keys:
        key = key.lower()
        if key in special_keys:
            formatted.append(f"<{key}>")
        else:
            formatted.append(key)

    return "+".join(formatted)

def main():
    validate_path()
    config = load_config()

    hotkey_combination = format_hotkey(config['hotkey'])

    with keyboard.GlobalHotKeys({
        hotkey_combination: launch_application
    }) as listener:
        listener.join()

if __name__ == "__main__":
    main()