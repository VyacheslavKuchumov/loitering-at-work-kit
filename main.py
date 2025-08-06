"""
Loitering at Work Kit

Usage:
    work.py --mousejiggle
    work.py --refresh
    work.py --mousejiggle --refresh

Options:
    --mousejiggle    Start the mouse jiggler
    --refresh        Start the mail/task refresher
    -h, --help       Show this help message and exit
"""

import time
import threading
import os
import argparse

import pyautogui       # pip install pyautogui
import keyboard        # pip install keyboard

def keyboard_listener():
    """
    Registers a global hotkey (Ctrl+Q) to immediately kill the process.
    """
    keyboard.add_hotkey('ctrl+q', lambda: os._exit(0))
    keyboard.wait()

def move_cursor(dx: int, dy: int, pause: float):
    """
    Move the mouse cursor by (dx, dy) instantly, then sleep for 'pause' seconds.
    """
    x, y = pyautogui.position()
    pyautogui.moveTo(x + dx, y + dy, duration=0)
    time.sleep(pause)

def jiggle_loop(delta: int = 40, pause: float = 0.1):
    """
    Continuously jiggle the mouse in a square pattern,
    pressing lock keys to simulate activity.
    """
    print("Mouse jiggler starting... Press CTRL+Q to quit.")
    while True:
        move_cursor(delta, 0, pause)
        pyautogui.press("capslock")
        move_cursor(0, delta, pause)
        pyautogui.press("numlock")
        move_cursor(-delta, 0, pause)
        pyautogui.press("capslock")
        move_cursor(0, -delta, pause)
        pyautogui.press("numlock")

def refresh_loop(mail_delay: int = 10, task_delay: int = 10):
    """
    Switch between email and task tracker tabs and refresh each periodically.
    """
    print("Mail refresher starting... Switch to your mail client/tab within 10 seconds.")
    time.sleep(mail_delay)
    while True:
        print("Refreshing mail...")
        pyautogui.press('f5')
        time.sleep(mail_delay)
        pyautogui.hotkey('ctrl', 'tab')
        time.sleep(1)

        print("Refreshing task tracker...")
        pyautogui.press('f12')
        time.sleep(task_delay)
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        time.sleep(1)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Loitering at Work Kit")
    parser.add_argument('--mousejiggle', action='store_true',
                        help='Start the mouse jiggler')
    parser.add_argument('--refresh', action='store_true',
                        help='Start the mail/task refresher')
    args = parser.parse_args()

    if not (args.mousejiggle or args.refresh):
        parser.print_help()
        return

    # Always start the hotkey listener
    listener = threading.Thread(target=keyboard_listener, daemon=True)
    listener.start()

    # Conditionally start worker threads
    if args.mousejiggle:
        jiggler = threading.Thread(target=jiggle_loop, daemon=True)
        jiggler.start()

    if args.refresh:
        refresher = threading.Thread(target=refresh_loop, daemon=True)
        refresher.start()

    # Keep alive until Ctrl+Q
    listener.join()

if __name__ == "__main__":
    main()