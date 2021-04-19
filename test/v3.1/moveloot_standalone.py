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
