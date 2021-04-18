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
        self.dunchk_momentum = 10
        self.target_relative_coords = [0, 0]
        self.current_player_coords = [0, 0]
        self.enemy_locs = []

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

        # The next block of code is setup for detecting the current player
        self.player_filter, player_custom_rect = grab_object_preset(
            object_name="player_map_loc")
        # initialize the WindowCapture class for player detection
        self.minimap_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", player_custom_rect)
        self.player_vision = Vision('playerv2_67.jpg')

        # The next block of code is setup for detecting enemies on minimap
        # This uses same image as player minimap but dupe it due to error prevent
        self.enemy_minimap_filter, enemy_custom_rect = grab_object_preset(
            object_name="enemy_map_locv3")
        self.enemy_minimap_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", enemy_custom_rect)
        # initialize the Vision class
        self.enemy_minimap_vision = Vision('enemy67.jpg')

        # The next block of code is setup for detecting if in a dungeon
        self.dunchk_filter, dunchk_custom_rect = grab_object_preset(
            object_name="dungeon_check")
        self.dunchk_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", dunchk_custom_rect)
        self.dunchk_vision = Vision('dunchk_67.jpg')

    def start_mainloop(self):
        # loop_time = time.time()
        time.sleep(0.1)
        while True:
            # print('FPS {}'.format(1 / (time.time() - loop_time)))
            # loop_time = time.time()
            if self.check_if_in_dungeon():
                if self.dunchk_momentum < 20:
                    self.dunchk_momentum += 1
                if self.check_for_enemies():
                    self.calc_nearest_enemy()
            elif self.dunchk_momentum >= 1:
                self.dunchk_momentum -= 1
            else:
                print("Exiting as ran out of momentum")
                break

    def check_if_in_dungeon(self):
        # print("Got to here")
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

    def check_for_enemies(self):
        minimap_screenshot = self.enemy_minimap_wincap.get_screenshot()
        # pre-process the image to help with detection
        enemy_output_image = self.enemy_minimap_vision.apply_hsv_filter(
            minimap_screenshot, self.enemy_minimap_filter)
        # do object detection, this time grab points
        enemy_rectangles = self.enemy_minimap_vision.find(
            enemy_output_image, threshold=0.61, epsilon=0.5)
        # then return answer to whether enemies are detected
        if len(enemy_rectangles) >= 1:
            # Need to first update the current player location
            self.can_find_current_player()
            points = self.enemy_minimap_vision.get_click_points(
                enemy_rectangles)
            # Then translate the points to be relative to the player
            points = self.get_relative_to_player(points)
            self.enemy_locs = points.copy()
            return True
        return False

    def calc_nearest_enemy(self):
        for x, y in self.enemy_locs:
            closest = 1000
            if x + y < closest:
                closest = x + y
                nearestx = x
                nearesty = y
        previous_angle = self.centre_mass_angle
        self.centre_mass_angle = self.grab_angle(
            nearestx, nearesty)
        if previous_angle != self.centre_mass_angle:
            print("Angle calc: x={}, y={}, angle={}".format(
                nearestx, nearesty, self.centre_mass_angle))
            # print(self.centre_mass_angle)

    def grab_angle(self, relx, rely):
        angle = math.degrees(math.atan2(rely, relx))
        if angle <= 90:
            angle = angle * -1 + 90
        else:
            angle = 360 + (angle-90) * -1
        # print("Angle calc: x={}, y={}, angle={}".format(relx, rely, angle))
        return angle

    def can_find_current_player(self):
        # Main logic for this method is below
        minimap_screenshot = self.enemy_minimap_wincap.get_screenshot()
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

    def get_relative_to_player(self, abs_list):
        # This will convert the points in a list
        # To be relative to the player
        playerx = self.current_player_coords[0]
        playery = self.current_player_coords[1]
        returnlist = []
        for x, y in abs_list:
            relx = x - playerx
            rely = playery - y
            returnlist.append([relx, rely])
        return returnlist


if __name__ == "__main__":
    cs = StandaloneCombat()
    cs.start_mainloop()
