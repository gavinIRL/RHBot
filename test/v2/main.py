# This will be the test file for the v2 bot
# As a reminder the features of this bot are intended to be the following:
# 1 - Ability to follow the existing player as per v1
# 2 - Ability to identify and pick up looton screen
# Note that this prelim loot pickup will not include a search
# for items that have dropped in the same area but off screen

import cv2 as cv
import os
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import grab_object_preset
from actionsv2 import Movement_Handler


class RHBotV2():
    def __init__(self, loot=True, loot_cd_max=5) -> None:
        # Initialise the variables for bot state (looting, moving)
        self.bot_state = "startup"
        # This is the variable for stopping the bot
        self.bot_running = False
        # This is the variable which enables or disables looting
        self.looting_enabled = loot
        # This is the variable which prevents getting stuck picking loot
        self.pressx_counter = 0
        # This is the variable which will track cooldown on searching for loot
        # After the bot has gotten stuck, format is seconds
        # The value assigned will correspond to time when lootsearch can recommence
        self.loot_cd = 0
        # And the variable which determines the cooldown each time
        self.loot_cd_max = loot_cd_max
        # This is the movement handler object
        self.movement = None

    def start(self):
        # Perform the prep required prior to main loop
        # Allow 3 seconds to open the game window
        sleep(3)
        self.bot_running = True

        # Change the working directory to the folder this script is in.
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Initialise the movement object and pass the state object
        self.movement = Movement_Handler(test_mode=False)

        # The next block of code is setup for detecting the other player

        # The next block of code is setup for detecting the current player

        # The next block of code is setup for detecting nearby loot

        # The next block of code is setup for detecting far loot

        # The next block of code is setup for detecting if there is a pressx prompt

        # The next block of code is setup for detecting if in a dungeon
        self.dunchk_filter, dunchk_custom_rect = grab_object_preset(
            object_name="dungeon_check")
        # This is only for testing and fixing the 150% screen scaling I have
        self.dunchk_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", dunchk_custom_rect)
        self.dunchk_vision = Vision('dunchk_67.jpg')

        # Start the movement bot
        self.movement.movement_start()
        # Start the loot bot

        # Begin the main loop

    def main_loop(self):
        while self.bot_running:

            # get an updated image of the game at specified area
            dunchk_screenshot = self.dunchk_wincap.get_screenshot()
            # pre-process the image to help with detection
            dunchk_output_image = self.dunchk_vision.apply_hsv_filter(
                dunchk_screenshot, self.dunchk_filter)
            # do object detection, this time grab the points
            dunchk_rectangles = self.dunchk_vision.find(
                dunchk_output_image, threshold=0.27, epsilon=0.5)

            if len(dunchk_rectangles) == 1:
                # Then grab an image to check for nearby loot
                # Filter the image
                # Verify if nearby loot detected
                if True:
                    # Press the x key to pickup the loot
                    self.pressx_counter += 1
                    # Need to prevent more than 6 attempts in a row
                    # Without movement signifying stuck loot
                    if self.pressx_counter == 5:
                        self.bot_state = "movement"

                # Grab the image to check for far loot
                # Filter the image
                # Check if any hits
                if True:
                    # Figure out closest item
                    # Move towards closest item
                    self.bot_state = "loot"
                # otherwise go back to movement mode to follow player
                else:
                    self.bot_state = "movement"
                    # Check for other player
                    if True:
                        # Check for current player
                        if True:
                            # Calculate relative position
                            # Move towards other player
                            pass
            # press 'q' with the output window focused to exit.
            # waits 1 ms every loop to process key presses
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                # stop movement
                self.movement.movement_stop()
                break
            # Have a key to disable or enable looting
            # Quick method of fixing a loot-seek loop
            if cv.waitKey(1) == ord('w'):
                self.looting_enabled = not self.looting_enabled
                print("Looting has been set to {}".format(self.looting_enabled))

    def stop(self):
        self.bot_running = False
