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
        # This is the variable which resets the keyboard and mouse periodically
        # Assume 1frame is ~15ms
        self.general_frames = 0
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

        # The next block of code is setup for detecting the other player
        self.othr_plyr_filter, othr_plyr_custom_rect = grab_object_preset(
            object_name="other_player_map_loc")
        self.othr_plyr_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", othr_plyr_custom_rect)
        self.othr_plyr_vision = Vision('otherplayer67.jpg')

        # The next block of code is setup for detecting the current player
        self.player_filter, player_custom_rect = grab_object_preset(
            object_name="player_map_loc")
        self.player_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", player_custom_rect)
        self.player_vision = Vision('playerv2_67.jpg')

        # The next block of code is setup for detecting enemies on minimap
        self.enemy_filter, enemy_custom_rect = grab_object_preset(
            object_name="enemy_map_locv3")
        self.enemy_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", enemy_custom_rect)
        self.enemy_vision = Vision('enemy67.jpg')

        # The next block of code is setup for detecting nearby loot
        self.lootnr_filter, lootnr_custom_rect = grab_object_preset(
            object_name="loot_near")
        self.lootnr_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", lootnr_custom_rect)
        self.lootnr_vision = Vision('lootnear67filt.jpg')

        # The next block of code is setup for detecting if in a dungeon
        self.dunchk_filter, dunchk_custom_rect = grab_object_preset(
            object_name="dungeon_check")
        self.dunchk_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", dunchk_custom_rect)
        self.dunchk_vision = Vision('dunchk_67.jpg')

        # The next block of code is setup for detecting if there is an x prompt
        self.xprompt_filter, xprompt_custom_rect = grab_object_preset(
            object_name="prompt_press_x_pickup")
        self.xprompt_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", xprompt_custom_rect)
        self.xprompt_vision = Vision("xprompt67filtv2.jpg")

        # Start the movement bot
        self.movement.movement_start()

    def move_mainloop(self):
        loop_time = time.time()
        while True:
            if self.check_if_in_dungeon():
                self.general_frames += 1
                if self.controller.combat_enabled:
                    if self.perform_enemy_check():
                        self.controller.mode = "combat"
                        break
                if self.controller.loot_enabled:
                    self.check_for_loot()
                self.move_to_other_player()
            else:
                sleep(0.4)

            if self.general_frames >= 75:
                Actions.move_mouse_centre()
                Actions.stop_keypresses(self.movement)
                self.general_frames = 0

            if 100*(loop_time - time.time()) < 1:
                # Minimum sleep time is roughly 15ms regardless
                time.sleep(0.001)
            loop_time = time.time()
        # After end stop all movement
        self.movement.movement_stop()

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
                    sleep(0.15)
                    Actions.press_key_once("x")
                    sleep(0.15)
                    while self.check_for_x_prompt():
                        self.pressx_counter += 2
                        # Press the x button thrice
                        Actions.press_key_once("x")
                        sleep(0.15)
                        Actions.press_key_once("x")
                        sleep(0.15)
                        Actions.press_key_once("x")
                        sleep(0.15)
                        if self.pressx_counter >= 5:
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
            lootnr_output_image, threshold=0.27, epsilon=0.5)
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
