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

    def convert_click_to_ratio(self, truex, truey):
        # This will grab the current rectangle coords of game window
        # and then turn the click values into a ratio of positions
        # versus the game window
        self.game_wincap.update_window_position(border=False)
        # Turn the screen pos into window pos
        relx = truex - self.game_wincap.window_rect[0]
        rely = truey - self.game_wincap.window_rect[1]
        # Then convert to a ratio
        ratx = relx/self.game_wincap.w
        raty = rely/self.game_wincap.h

        return ratx, raty

    def convert_ratio_to_click(self, ratx, raty):
        # This will grab the current rectangle coords of game window
        # and then turn the ratio of positions versus the game window
        # into true x,y coords
        self.game_wincap.update_window_position(border=False)
        # Turn the ratios into relative
        relx = int(ratx * self.game_wincap.w)
        rely = int(raty * self.game_wincap.h)
        # Turn the relative into true
        truex = relx + self.game_wincap.window_rect[0]
        truey = rely + self.game_wincap.window_rect[1]
        return truex, truey

    def on_click(self, x, y, button, pressed):
        # when pressed is False, that means it's a release event.
        # let's listen only to mouse click releases
        if not pressed:
            # Need to get the ratio compared to window top left
            # This will allow common usage on other size monitors
            print("x={}, y={}".format(x, y))
            xratio, yratio = self.convert_click_to_ratio(x, y)
            print("xrat={}, yrat={}".format(xratio, yratio))
            xconv, yconv = self.convert_ratio_to_click(xratio, yratio)
            print("xconv={}, yconv={}".format(xconv, yconv))

    def start(self):
        self.start_mouse_listener()
        while True:
            time.sleep(1)


if __name__ == "__main__":
    mt = MouseTest()
    mt.start()
