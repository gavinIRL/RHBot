import pydirectinput as pdi
import time
import os
import json
import numpy as np
from v1.bot_utils import WindowCapture
import cv2 as cv


class FollowerBot():
    def __init__(self) -> None:
        pdi.FAILSAFE = True
        # The variable that will keep track of the position of player 1 and 2
        self.target_pos = {0, 0}
        self.current_pos = {0, 0}
        # Set up the keys for movement and control

    def main(self):
        # First detect the current player 1 and player 2 location
        self.target_pos = self.detect_other_player_loc()
        self.current_pos = self.detect_bot_loc()
        # Change the working directory to the folder this script is in.
        # Doing this because I'll be putting the files from each video in their own folder on GitHub
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # initialize the WindowCapture class
        wincap = WindowCapture('Untitled - Notepad')

        loop_time = time.time()
        while(True):

            # get an updated image of the game
            screenshot = wincap.get_screenshot()

            cv.imshow('Computer Vision', screenshot)

            # debug the loop rate
            print('FPS {}'.format(1 / (time.time() - loop_time)))
            loop_time = time.time()

            # press 'q' with the output window focused to exit.
            # waits 1 ms every loop to process key presses
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

        print('Done.')

    def detect_other_player_loc(self):
        return False

    def detect_bot_loc(self):
        return False


if __name__ == "__main__":
    rhb = FollowerBot()
    rhb.main()
