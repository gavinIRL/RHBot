# This will be the upgraded v2 move and loot only file
# But with quick restart capability and modular design
# No longer meant to be used as main file

import cv2 as cv
import os
from time import time, sleep
import numpy as np
from pynput.keyboard import Key, Listener, KeyCode
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import grab_object_preset
from actionsv2 import Movement_Handler, Actions


class StandaloneMoveLoot():
    def __init__(self, controller, loot_cd_max=5) -> None:
        self.controller = controller
        # This is the variable which prevents getting stuck picking loot
        self.pressx_counter = 0
        # This is the variable which will track cooldown on searching for loot
        # After the bot has gotten stuck, format is seconds
        # The value assigned will correspond to time when lootsearch can recommence
        self.near_loot_cd = 0
        # And the variable which determines the cooldown each time
        self.near_loot_cd_max = loot_cd_max
        # This will hold the relative location of the other player
        self.other_player_rel_coords = [0, 0]
        # This will hold the location of the current player
        self.current_player_coords = [0, 0]
        # The variable for ensuring momentum of player movement
        self.movement_frames = 0
        self.momentum = 0
        self.max_momentum = 2
        self.momentum_accel = 10
        # Variable for ensuring positive enemy detection
        self.enemy_detect_frames = 0

        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        # XX  Now time to initialise all of the required objects  XX
        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        # Initialise the movement object and pass the state object
        self.movement = Movement_Handler(test_mode=False)

        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # Grab the gamename from the text file
        with open("gamename.txt") as f:
            gamename = f.readline()

        # The next block of code is setup for detecting the other player
        self.othr_plyr_filter, othr_plyr_custom_rect = grab_object_preset(
            object_name="other_player_map_loc")
        self.othr_plyr_wincap = WindowCapture(
            gamename, othr_plyr_custom_rect)
        self.othr_plyr_vision = Vision('otherplayer67.jpg')

        # The next block of code is setup for detecting the current player
        self.player_filter, player_custom_rect = grab_object_preset(
            object_name="player_map_loc")
        self.player_wincap = WindowCapture(
            gamename, player_custom_rect)
        self.player_vision = Vision('playerv2_67.jpg')

        # The next block of code is setup for detecting enemies on minimap
        self.enemy_filter, enemy_custom_rect = grab_object_preset(
            object_name="enemy_map_locv3")
        self.enemy_wincap = WindowCapture(
            gamename, enemy_custom_rect)
        self.enemy_vision = Vision('enemy67.jpg')

        # The next block of code is setup for detecting nearby loot
        self.lootnr_filter, lootnr_custom_rect = grab_object_preset(
            object_name="loot_near")
        self.lootnr_wincap = WindowCapture(
            gamename, lootnr_custom_rect)
        self.lootnr_vision = Vision('lootnear67filt.jpg')

        # The next block of code is setup for detecting if in a dungeon
        self.dunchk_filter, dunchk_custom_rect = grab_object_preset(
            object_name="dungeon_check")
        self.dunchk_wincap = WindowCapture(
            gamename, dunchk_custom_rect)
        self.dunchk_vision = Vision('dunchk_67.jpg')

        # The next block of code is setup for detecting if there is an x prompt
        self.xprompt_filter, xprompt_custom_rect = grab_object_preset(
            object_name="prompt_press_x_pickup")
        self.xprompt_wincap = WindowCapture(
            gamename, xprompt_custom_rect)
        self.xprompt_vision = Vision("xprompt67filtv2.jpg")

        # Start the movement bot
        self.movement.movement_start()

    def move_mainloop(self):
        loop_time = time()
        reset_time = time() + 5
        while True:
            if self.check_if_in_dungeon():
                if self.controller.combat_enabled:
                    if self.perform_enemy_check():
                        self.controller.mode = "combat"
                        break
                if self.controller.loot_enabled:
                    self.check_for_loot()
                self.move_to_other_player()
            else:
                sleep(0.4)

            if (time() - reset_time) > 0:
                Actions.move_mouse_centre()
                Actions.stop_keypresses(self.movement)
                reset_time = time() + 5

            # If loops are over 100fps, slow to 67fps
            if 100*(time() - loop_time) < 1:
                # Minimum sleep time is roughly 15ms regardless
                sleep(0.001)
            loop_time = time()
        # After end stop all movement
        self.movement.movement_stop()

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

    def perform_enemy_check(self):
        if self.check_for_enemies():
            self.enemy_detect_frames += 1
            if self.enemy_detect_frames >= 2:
                return True
        else:
            self.enemy_detect_frames = 0
        return False

    def check_for_enemies(self):
        enemy_screenshot = self.enemy_wincap.get_screenshot()
        # pre-process the image to help with detection
        enemy_output_image = self.enemy_vision.apply_hsv_filter(
            enemy_screenshot, self.enemy_filter)
        # do object detection, this time grab points
        enemy_rectangles = self.enemy_vision.find(
            enemy_output_image, threshold=0.61, epsilon=0.5)
        # then return answer to whether enemies are detected
        if len(enemy_rectangles) >= 1:
            return True
        return False

    def check_for_loot(self):
        if not self.check_if_loot_cooldown():
            if self.check_if_nearby_loot():
                # Now need to check if there is a prompt
                if self.check_for_x_prompt():
                    # Need to stop all movement
                    self.movement.movement_update_xy(0, 0)
                    # Clear all button presses
                    Actions.move_mouse_centre()
                    Actions.stop_keypresses(self.movement)
                    # Press x a couple times off the bat
                    Actions.press_key_once("x")
                    sleep(0.6)
                    while self.check_for_x_prompt():
                        self.pressx_counter += 1
                        # Press the x button once
                        Actions.press_key_once("x")
                        sleep(0.6)
                        if self.pressx_counter >= 8:
                            self.near_loot_cd = time() + self.near_loot_cd_max
                            break
                        Actions.stop_keypresses(self.movement)
            self.pressx_counter = 0

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
            lootnr_output_image, threshold=0.31, epsilon=0.5)
        # then return answer to whether currently in dungeon
        if len(lootnr_rectangles) >= 1:
            return True
        return False

    def check_for_x_prompt(self):
        # get an updated image of the game at specified area
        xprompt_screenshot = self.xprompt_wincap.get_screenshot()
        # pre-process the image to help with detection
        xprompt_output_image = self.xprompt_vision.apply_hsv_filter(
            xprompt_screenshot, self.xprompt_filter)
        # do object detection, this time grab rectangles
        xprompt_rectangles = self.xprompt_vision.find(
            xprompt_output_image, threshold=0.61, epsilon=0.5)
        # then return answer to whether currently in dungeon
        if len(xprompt_rectangles) == 1:
            return True
        return False

    # Having these be separate methods as main loop too bulky
    def can_find_both_players(self):
        # This will return true if both players could be found
        # Otherwise will set relative to 0,0 and return false
        if self.can_find_other_player():
            if self.can_find_current_player():
                return True
            # Need to use last known position otherwise
            return True
        return False

    def can_find_current_player(self):
        # Main logic for this method is below
        minimap_screenshot = self.player_wincap.get_screenshot()
        player_image = self.player_vision.apply_hsv_filter(
            minimap_screenshot, self.player_filter)
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

    def can_find_other_player(self):
        # then try to detect the other player
        minimap_screenshot = self.othr_plyr_wincap.get_screenshot()
        output_image = self.othr_plyr_vision.apply_hsv_filter(
            minimap_screenshot, self.othr_plyr_filter)
        # do object detection, this time grab the points
        rectangles = self.othr_plyr_vision.find(
            output_image, threshold=0.41, epsilon=0.5)
        points = self.othr_plyr_vision.get_click_points(rectangles)
        if len(points) == 1:
            self.other_player_rel_coords[0] = points[0][0] - \
                self.current_player_coords[0]
            self.other_player_rel_coords[1] = self.current_player_coords[1] - points[0][1]
            return True
        elif len(points) >= 2:
            # Will grab the point closest to the centre of the minimap and track that
            # Allowing some small amount of redundancy for short-range following
            # In event that the background is also picked up
            middle_x = 0
            middle_y = 0
            dist = 1000
            for x, y in points:
                if (x+y) < dist:
                    dist = x+y
                    middle_x = x
                    middle_y = y
            self.other_player_rel_coords[0] = middle_x - \
                self.current_player_coords[0]
            self.other_player_rel_coords[1] = self.current_player_coords[1] - middle_y
            return True
        else:
            # Should this be set to 0,0 or left as is? Come back to this later
            # Maybe set it to the current player coords instead
            # self.other_player_rel_coords = [0, 0]
            return False

    def move_to_other_player(self):
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
