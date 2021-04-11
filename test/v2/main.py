# This will be the test file for the v2 bot
# As a reminder the features of this bot are intended to be the following:
# 1 - Ability to follow the existing player as per v1
# 2 - Ability to identify and pick up looton screen
# Note that this prelim loot pickup will not include a search
# for items that have dropped in the same area but off screen

import cv2 as cv
import os
from time import time, sleep
import numpy as np
from pynput.keyboard import Key, Listener, KeyCode
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import grab_object_preset
from actionsv2 import Movement_Handler, Actions

# Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


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
        # This is the variable which prevents getting stuck trying to
        # Access inaccessible loot, assume 1frame is ~10ms
        self.loot_movement_frames = 0
        # This is the variable which resets the keyboard and mouse periodically
        # Assume 1frame is ~10ms
        self.general_frames = 0
        # This is the variable which will track cooldown on searching for loot
        # After the bot has gotten stuck, format is seconds
        # The value assigned will correspond to time when lootsearch can recommence
        self.near_loot_cd = 0
        # And the variable which determines the cooldown each time
        self.near_loot_cd_max = loot_cd_max
        # This is the movement handler object
        self.movement = None
        # This will hold the location of the nearest loot identified
        self.nearest_loot_coords = [0, 0]
        # This will hold the location of the other player
        self.other_player_rel_coords = [0, 0]
        # This will hold the location of the current player
        self.current_player_coords = [0, 0]
        # This will be the shared screenshot for detecting both players
        self.player_screenshot = None
        # The variables for shortcuts such as terminating bot, etc.
        self.listener = None
        # The variable for ensuring momentum of player movement
        self.movement_frames = 0
        self.momentum = 0
        self.max_momentum = 2
        self.momentum_accel = 10
        # The variable for ensuring positive nearloot detection
        # Requires at least 2 positive frames in a row to start action
        self.near_loot_positive_frames = 0

    def start(self):
        # Perform the prep required prior to main loop
        # Allow 3 seconds to open the game window
        sleep(3)

        # Initialise the movement object and pass the state object
        self.movement = Movement_Handler(test_mode=False)

        # The next block of code is setup for detecting the other player
        self.object_filter, object_custom_rect = grab_object_preset(
            object_name="other_player_map_loc")
        # initialize the WindowCapture class for object detection
        self.object_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", object_custom_rect)
        # initialize the Vision class
        self.object_vision = Vision('otherplayer67.jpg')

        # The next block of code is setup for detecting the current player
        self.player_filter, _ = grab_object_preset(
            object_name="player_map_loc")
        self.player_vision = Vision('playerv2_67.jpg')

        # The next block of code is setup for detecting nearby loot
        self.lootnr_filter, lootnr_custom_rect = grab_object_preset(
            object_name="loot_near")
        self.lootnr_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", lootnr_custom_rect)
        self.lootnr_vision = Vision('lootnear67filt.jpg')

        # The next block of code is setup for detecting far loot
        self.lootfr_filter, lootfr_custom_rect = grab_object_preset(
            object_name="loot_far")
        self.lootfr_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", lootfr_custom_rect)
        self.lootfr_vision = Vision('lootfar67filt.jpg')

        # The next block of code is setup for detecting if in a dungeon
        self.dunchk_filter, dunchk_custom_rect = grab_object_preset(
            object_name="dungeon_check")
        self.dunchk_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", dunchk_custom_rect)
        self.dunchk_vision = Vision('dunchk_67.jpg')

        # Start the movement bot
        self.movement.movement_start()

        # Begin the main loop
        self.bot_running = True
        self.main_loop()

    def main_loop(self):
        # self.start_keypress_listener()
        while self.bot_running:
            if self.check_if_in_dungeon():
                self.general_frames += 1
                if self.looting_enabled:
                    self.check_for_loot()
                else:
                    self.bot_state = "movement"
                # Perform movement towards other player
                if self.bot_state == "movement":
                    self.move_to_other_player()
            else:
                # print("Not in dungeon")
                sleep(0.5)
            # Reset the mouse and keypresses every so often
            if self.general_frames >= 75:
                Actions.move_mouse_centre()
                Actions.stop_keypresses(self.movement)
                self.general_frames = 0
        cv.destroyAllWindows()
        self.movement.movement_stop()

    def start_keypress_listener(self):
        if self.listener == None:
            self.listener = Listener(on_press=self.on_press,
                                     on_release=self.on_release, suppress=True)
            self.listener.start()

    def on_press(self, key):
        if key == KeyCode(char='q'):
            cv.destroyAllWindows()
            self.bot_running = False
            return False
        if key == KeyCode(char='w'):
            self.looting_enabled = not self.looting_enabled
            print("Looting has been set to {}".format(self.looting_enabled))

    def on_release(self, key):
        # Do nothing
        pass

    def check_for_loot(self):
        if not self.check_if_loot_cooldown():
            if self.check_if_nearby_loot():
                # Now need to check if there is a prompt
                if self.check_for_x_prompt():
                    # Ensure there are at least 2 frames in a row
                    self.near_loot_positive_frames += 1
                    if self.near_loot_positive_frames >= 2:
                        # Need to stop all movement
                        self.movement.movement_update_xy(0, 0)
                        # And then set the bot state to looting
                        self.bot_state = "loot"
                        # Clear all button presses
                        Actions.move_mouse_centre()
                        Actions.stop_keypresses(self.movement)
                        while self.check_if_nearby_loot():
                            self.pressx_counter += 1
                            # Press the x button
                            Actions.press_key_once("x")
                            sleep(0.3)
                            if self.pressx_counter >= 10:
                                self.near_loot_cd = time() + self.near_loot_cd_max
                                break
                        Actions.stop_keypresses(self.movement)
            # elif self.loot_movement_frames >= 80:
            #     self.near_loot_cd = time() + self.near_loot_cd_max
            #     self.bot_state = "movement"
            # elif self.check_if_far_loot():
            #     self.loot_movement_frames += 1
            #     self.bot_state = "loot"
            #     relx, rely = self.nearest_loot_coords
            #     self.movement.movement_update_xy(relx, rely)
            else:
                self.bot_state = "movement"
            self.near_loot_positive_frames = 0
            self.pressx_counter = 0
        else:
            self.bot_state = "movement"

    def move_to_other_player(self):
        # print("Trying to find both players")
        self.loot_movement_frames = 0
        if self.can_find_both_players():
            relx, rely = self.other_player_rel_coords
            self.movement.movement_update_xy(relx, rely)
            self.movement_frames += 1
            if self.movement_frames % self.momentum_accel == 0:
                if not self.momentum >= self.max_momentum:
                    self.momentum += 1
        else:
            if self.momentum < 1:
                self.movement.movement_update_xy(0, 0)
                self.momentum = 0
                # Have the consecutive move count only reset if momentum gone
                self.movement_frames = 0
            else:
                self.momentum -= 1
                # Only slightly remove the momentum progress
                self.movement_frames -= (int(self.momentum_accel/2))

    def stop(self):
        self.bot_running = False

    # Having these be separate methods as main loop too bulky
    def can_find_both_players(self):
        # This will return true if both players could be found
        # Otherwise will set relative to 0,0 and return false
        if self.can_find_other_player():
            if self.can_find_current_player():
                return True
        return False

    def can_find_other_player(self):
        # get an updated image of the game at map loc
        self.player_screenshot = self.object_wincap.get_screenshot()
        # then try to detect the other player
        output_image = self.object_vision.apply_hsv_filter(
            self.player_screenshot, self.object_filter)
        # do object detection, this time grab the points
        rectangles = self.object_vision.find(
            output_image, threshold=0.41, epsilon=0.5)
        points = self.object_vision.get_click_points(rectangles)
        if len(points) == 1:
            self.other_player_rel_coords[0] = points[0][0] - \
                self.current_player_coords[0]
            self.other_player_rel_coords[1] = self.current_player_coords[1] - points[0][1]
            return True
        else:
            # Should this be set to 0,0 or left as is? Come back to this later
            # Maybe set it to the current player coords instead
            self.other_player_rel_coords = [0, 0]
            return False

    def can_find_current_player(self):
        # Will make this forward compatible for multiple modes e.g. enemy detection
        # Have placeholder for now
        combat_mode = False
        if combat_mode:
            self.player_screenshot = self.object_wincap.get_screenshot()
        # Main logic for this method is below
        player_image = self.player_vision.apply_hsv_filter(
            self.player_screenshot, self.player_filter)
        player_rectangles = self.player_vision.find(
            player_image, threshold=0.41, epsilon=0.5)
        player_points = self.player_vision.get_click_points(
            player_rectangles)
        if len(player_points) == 1:
            self.current_player_coords[0] = player_points[0][0]
            self.current_player_coords[1] = player_points[0][1]
            return True
        else:
            # Should this be set to 0,0 or left as is? Come back to this later
            # Will leave as is for now, probably useful for enemy detect
            return False

    def check_if_in_dungeon(self):
        # get an updated image of the game at specified area
        dunchk_screenshot = self.dunchk_wincap.get_screenshot()
        # pre-process the image to help with detection
        dunchk_output_image = self.dunchk_vision.apply_hsv_filter(
            dunchk_screenshot, self.dunchk_filter)
        # do object detection, this time grab rectangles
        dunchk_rectangles = self.dunchk_vision.find(
            dunchk_output_image, threshold=0.31, epsilon=0.5)
        # then return answer to whether currently in dungeon
        if len(dunchk_rectangles) == 1:
            return True
        return False

    def check_if_loot_cooldown(self):
        if not self.near_loot_cd == 0:
            if (self.near_loot_cd-time()) < 0:
                self.near_loot_cd = 0
                return False
            return True

    def check_if_nearby_loot(self):
        # get an updated image of the game at specified area
        lootnr_screenshot = self.lootnr_wincap.get_screenshot()
        # pre-process the image to help with detection
        lootnr_output_image = self.lootnr_vision.apply_hsv_filter(
            lootnr_screenshot, self.lootnr_filter)
        # do object detection, this time grab rectangles
        lootnr_rectangles = self.lootnr_vision.find(
            lootnr_output_image, threshold=0.27, epsilon=0.5)
        # then return answer to whether currently in dungeon
        if len(lootnr_rectangles) >= 1:
            return True
        return False

    def check_if_far_loot(self):
        # get an updated image of the game at specified area
        lootfr_screenshot = self.lootfr_wincap.get_screenshot()
        # pre-process the image to help with detection
        lootfr_output_image = self.lootfr_vision.apply_hsv_filter(
            lootfr_screenshot, self.lootfr_filter)
        # do object detection, this time grab rectangles
        lootfr_rectangles = self.lootfr_vision.find(
            lootfr_output_image, threshold=0.31, epsilon=0.5)
        # then return answer to whether currently in dungeon
        if len(lootfr_rectangles) >= 1:
            points = self.lootfr_vision.get_click_points(lootfr_rectangles)
            # Need to calc the coords of the nearest loot
            minx, miny, mindist = [1000, 1000, 10000]
            for x, y in points:
                # These are the approximate player feet location
                # Pickup radius is large enough that won't be a major issue
                relx = 640-x
                rely = y-521
                # Assuming y pixel values are twice distance of x values
                # Due to the ~30-35deg angle of the view
                dist = rely+relx
                if dist < mindist:
                    mindist = dist
                    minx = relx
                    miny = rely
            # Approx conversion from minimap to mainscreen is 1/20
            # However it updates frequently enough that it'll get there eventually
            # Worst case would be making too small steps between updates
            # Therefore will use /15 instead of /20
            self.nearest_loot_coords = [int(minx/15), int(miny/15)]
            return True
        return False


if __name__ == "__main__":
    rhbv2 = RHBotV2(loot=True)
    rhbv2.start()
