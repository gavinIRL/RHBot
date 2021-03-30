import pydirectinput as pdi
import time
import os
import json
import numpy as np


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

    def detect_other_player_loc(self):
        pass

    def detect_bot_loc(self):
        pass


if __name__ == "__main__":
    rhb = FollowerBot()
    rhb.main()
