# This file is for testing and verifying the ratio-to-true calculation
# It will be done in real-time rather than as part of test 5
# As it will be much quicker to debug for #54

import pyautogui
import sys
import time
from windowcapture import WindowCapture
import os
print('Press Ctrl-C to quit.')


class ConvertTest():

    def __init__(self) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        with open("gamename.txt") as f:
            gamename = f.readline()
        self.game_wincap = WindowCapture(gamename)
        # self.rely = 0

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

    def start(self):
        try:
            while True:
                x, y = pyautogui.position()
                ratx, raty = self.convert_click_to_ratio(x, y)
                # ratx = "{:.2f}".format(ratx)
                # raty = "{:.2f}".format(raty)
                convx, convy = self.convert_ratio_to_click(
                    float(ratx), float(raty))
                positionStr = 'X: ' + \
                    str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
                # positionStr += ' ratX: ' + \
                #     str(ratx).rjust(4) + ' ratY: ' + str(raty).rjust(4)
                positionStr += ' convX: ' + \
                    str(convx).rjust(4) + ' convY: ' + str(convy).rjust(4)
                # positionStr += ' relY: ' + \
                #     str(self.rely).rjust(4) + ' winY: ' + \
                #     str(self.game_wincap.window_rect[1]).rjust(4)

                print(positionStr, end='')
                print('\b' * len(positionStr), end='', flush=True)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print('\n')


if __name__ == "__main__":
    ct = ConvertTest()
    ct.start()
