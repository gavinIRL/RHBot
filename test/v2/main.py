# This will be the test file for the v2 bot
# As a reminder the features of this bot are intended to be the following:
# 1 - Ability to follow the existing player as per v1
# 2 - Ability to identify and pick up looton screen
# Note that this prelim loot pickup will not include a search
# for items that have dropped in the same area but off screen

import os
from time import time, sleep


class RHBotV2():
    def __init__(self, loot=True) -> None:
        # Initialise the variables for bot state (looting, moving)
        self.bot_state = "startup"
        # This is the variable for stopping the bot
        self.bot_running = False
        # This is the variable which enables or disables looting
        self.looting = loot

    def start(self):
        # Perform the prep required prior to main loop
        # Allow 3 seconds to open the game window
        sleep(3)

        # Change the working directory to the folder this script is in.
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Initialise the actions object

        # The next block of code is setup for detecting the other player

        # The next block of code is setup for detecting the current player

        # The next block of code is setup for detecting the loot

        # The next block of code is setup for detecting if in a dungeon

        # Start the movement bot
        # Start the loot bot

        # Begin the main loop

    def main_loop(self):
        pass

    def stop(self):
        pass
