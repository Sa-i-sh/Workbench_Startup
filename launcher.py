from pynput import keyboard
import json
import os
import subprocess
import time
from dotenv import load_dotenv

load_dotenv()

pressed_keys = set()
triggered_combos = set()

CTRL_CHAR_MAP = {
    "\x01": "a",  
    "\x02": "b",  
    "\x03": "c",  
    "\x04": "d",  
    "\x05": "e",  
    "\x06": "f",  
    "\x07": "g",  
    "\x08": "h",  
    "\x09": "i",  
    "\x0a": "j",  
    "\x0b": "k",  
    "\x0c": "l",  
    "\x0d": "m", 
    "\x0e": "n",  
    "\x0f": "o",  
    "\x10": "p",  
    "\x11": "q",  
    "\x12": "r",  
    "\x13": "s",  
    "\x14": "t",  
    "\x15": "u",  
    "\x16": "v",  
    "\x17": "w",  
    "\x18": "x",  
    "\x19": "y",  
    "\x1a": "z",  
}

def load_config():
    with open("config.json", "r") as file:
        return json.load(file)


def execute_actions(actions, delay):

    for action in actions:
        if action["type"] == "browser":
            chrome_path = os.getenv("CHROME_PATH")
            subprocess.Popen([chrome_path, action["url"]])

        elif action["type"] == "app":
            app_path = os.getenv(action["env_key"])
            subprocess.Popen([app_path])

        time.sleep(delay)


def normalize_key(key):

    if isinstance(key, keyboard.Key):
        name = str(key).replace("Key.", "").lower()

        if name in ["ctrl_l", "ctrl_r"]:
            return "ctrl"

        if name in ["shift_l", "shift_r"]:
            return "shift"

        if name in ["alt_l", "alt_r"]:
            return "alt"

        return name

    elif isinstance(key, keyboard.KeyCode):

        if key.char is None:
            return None

        c = key.char.lower()

        if c in CTRL_CHAR_MAP:
            return CTRL_CHAR_MAP[c]

        return c

    return None


def main():
    config = load_config()
    shortcuts = config["shortcuts"]
    delay = config["launch_delay"]

    combo_map = {
        frozenset(s["hotkey"]): s["actions"]
        for s in shortcuts
    }

    def on_press(key):

        k = normalize_key(key)

        if not k:
            return

        pressed_keys.add(k)

        for combo, actions in combo_map.items():

            if combo.issubset(pressed_keys):

                if combo not in triggered_combos:
                    execute_actions(actions, delay)
                    triggered_combos.add(combo)

                    pressed_keys.clear()
                    triggered_combos.clear()
                    break

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()