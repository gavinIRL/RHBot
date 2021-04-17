# The intent of this test is to verify that a standalone combat bot works
# And then incorporate the working standalone back into the v3 test bot
from hsvfilter import grab_object_preset
from windowcapture import WindowCapture
from vision import Vision
import os
import combo
import threading
import time
import pydirectinput
import math

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class StandaloneCombat():
    def __init__(self) -> None:
        self.combo_queue = []
        self.nearest_enemy_dist = 1
        self.dist_threshold = 125
        self.centre_mass_angle = 90
        self.ongoing_combo_count = False
        self.frames_since_combo_detect = 1000
        self.dunchk_momentum = 0
        self.target_relative_coords = [0, 0]

        self.setup()

    def setup(self):

        # The next block of code is setup for detecting the section cleared msg
        self.sect_clear_filter, sect_clear_custom_rect = grab_object_preset(
            sect_clear_name="message_section_cleared")
        # initialize the WindowCapture class for sect_clear detection
        self.sect_clear_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", sect_clear_custom_rect)
        # initialize the Vision class
        self.sect_clear_vision = Vision('SectionCleared67.jpg')

        # The next block of code is setup for detecting the combo count
        self.combo_count_filter, combo_count_custom_rect = grab_object_preset(
            combo_count_name="combo_count")
        # initialize the WindowCapture class for combo_count detection
        self.combo_count_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", combo_count_custom_rect)
        # initialize the Vision class
        self.combo_count_vision = Vision('combocount67.jpg')
