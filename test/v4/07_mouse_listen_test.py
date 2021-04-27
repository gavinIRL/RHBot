# This file is an extension of test_06 meant to solve #54
# This will output the ratio, etc. when user clicks
from pynput import mouse
import time
import os
from windowcapture import WindowCapture
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class MouseTest():
    def __init__(self) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open("gamename.txt") as f:
            gamename = f.readline()
        self.game_wincap = WindowCapture(gamename)

    def start_mouse_listener(self):
        self.mouse_listener = mouse.Listener(
            on_click=self.on_click)
        self.mouse_listener.start()
        self.mouse_listener.wait()

    def start(self):
        while True:
            time.sleep(1)


if __name__ == "__main__":
    mt = MouseTest()
    mt.start()
