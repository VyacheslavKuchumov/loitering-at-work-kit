import time
import threading
import pyautogui
import os
import keyboard       # pip install keyboard

def keyboard_listener():
    """
    Registers global hotkeys for 'q' and 'ctrl+q'.
    Pressing either will immediately kill the whole process.
    """
    # 'Ctrl+Q'
    keyboard.add_hotkey('ctrl+q', lambda: os._exit(0))
    # Keep the thread alive so hooks stay registered
    keyboard.wait()

def refresh_loop():
    """
    Your mail/task refresh cycle, running continuously until
    'q' or 'Ctrl+Q' is pressed.
    """
    print("Switch to the email. Waiting 10 seconds...")
    time.sleep(10)

    while True:
        print("Refreshing the mail!")
        pyautogui.press('f5')
        time.sleep(10)

        pyautogui.hotkey('ctrl', 'tab')
        time.sleep(1)

        print("Refreshing the task tracker!")
        pyautogui.press('f12')
        time.sleep(10)

        pyautogui.hotkey('ctrl', 'shift', 'tab')
        time.sleep(1)

def main():
    # Start the hotkey listener as a daemon
    listener = threading.Thread(target=keyboard_listener, daemon=True)
    listener.start()

    # Start your refresh cycle as another daemon
    refresher = threading.Thread(target=refresh_loop, daemon=True)
    refresher.start()

    # Keep the main thread alive indefinitely
    listener.join()

if __name__ == "__main__":
    main()
