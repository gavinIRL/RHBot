import pydirectinput as pdi
import time
import os
import json
import numpy as np


class FollowerBot():
    def __init__(self) -> None:
        pdi.FAILSAFE = True
        # The variable that will keep track of the zones
        self.current_zone = 0
        # The variable that will estimate from the map the current position
        # Used for checking if within attacking distance
        # And also used for calculating what buttons to press to travel to the next area
        self.current_pos = {0, 0}

        # These will hold the current skill cooldown finish times
        self.cooldown_end_time = {
            "a": 0, "b": 0, "d": 0, "f": 0, "g": 0, "h": 0
        }


if __name__ == "__main__":
    rhb = FollowerBot()
    rhb.main()
