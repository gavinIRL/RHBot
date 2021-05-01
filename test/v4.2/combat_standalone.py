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
import cv2 as cv
from win32api import GetSystemMetrics
import ctypes

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class StandaloneCombat():
    # Weapon arg options are 2 letter for weapon and then either
    # F or U for focused or unfocused
    def __init__(self, controller, weapon="MSU", level=1) -> None:
        self.controller = controller
        # self.nearest_enemy_dist = 1
        self.dist_threshold = 125
        self.centre_mass_angle = 90
        # self.ongoing_combo_count = False
        # self.frames_since_combo_detect = 1000
        self.dunchk_momentum = 10
        self.target_relative_coords = [0, 0]
        self.current_player_coords = [0, 0]
        self.other_player_rel_coords = [0, 0]
        self.enemy_locs = []
        self.running = False

        self.setup()

        # This will decide which class to use
        self.weapon = weapon
        # This will assign correct skills for level
        self.level = level
        # This will hold the cooldown times for each skill
        self.cooldowns = {"popthis": 1}
        # This will track when a key can be next pressed
        self.cd_tracker = {"popthis": 1}
        # This will be the class to use
        self.combos = None
        # This will be hold the current keypress queue
        self.combo_queue = []
        # This method fills out each of the above vars
        self.initialise_wep_class()

    def setup(self):

        # Grab the gamename from the text file
        with open("gamename.txt") as f:
            gamename = f.readline()

        # Find out the display scaling - either 100% or 150%
        scaling = self.get_monitor_scaling()

        # The next block of code is setup for detecting the section cleared msg
        self.sect_clear_filter, sect_clear_custom_rect = grab_object_preset(
            object_name="message_section_cleared")
        # initialize the WindowCapture class for sect_clear detection
        self.sect_clear_wincap = WindowCapture(
            gamename, sect_clear_custom_rect)
        # initialize the Vision class
        self.sect_clear_vision = Vision('SectionCleared67.jpg')

        # The next block of code is setup for detecting the combo count
        self.combo_count_filter, combo_count_custom_rect = grab_object_preset(
            object_name="combo_count")
        # initialize the WindowCapture class for combo_count detection
        self.combo_count_wincap = WindowCapture(
            gamename, combo_count_custom_rect)
        # initialize the Vision class
        self.combo_count_vision = Vision('combocount67.jpg')

        # The next block of code is setup for detecting the current player
        self.player_filter, player_custom_rect = grab_object_preset(
            object_name="player_map_loc")
        # initialize the WindowCapture class for player detection
        self.player_wincap = WindowCapture(
            gamename, player_custom_rect)
        self.player_vision = Vision('playerv2_67.jpg')

        # The next block of code is setup for detecting enemies on minimap
        # This uses same image as player minimap but dupe it due to error prevent
        self.enemy_minimap_filter, enemy_custom_rect = grab_object_preset(
            object_name="enemy_map_locv3")
        self.enemy_minimap_wincap = WindowCapture(
            gamename, enemy_custom_rect)
        # initialize the Vision class
        self.enemy_minimap_vision = Vision('enemy67.jpg')

        # The next block of code is setup for detecting if in a dungeon
        self.dunchk_filter, dunchk_custom_rect = grab_object_preset(
            object_name="dungeon_check")
        self.dunchk_wincap = WindowCapture(
            gamename, dunchk_custom_rect)
        self.dunchk_vision = Vision('dunchk_67.jpg')

        # The next block of code is setup for detecting the other player
        self.othr_plyr_filter, othr_plyr_custom_rect = grab_object_preset(
            object_name="other_player_map_loc")
        self.othr_plyr_wincap = WindowCapture(
            gamename, othr_plyr_custom_rect)
        self.othr_plyr_vision = Vision('otherplayer67.jpg')

    def combat_mainloop(self):
        loop_time = time.time()
        time.sleep(0.1)
        # Need to start the combo
        self.start_combo_handler()
        while True:
            if self.check_if_in_dungeon():
                if self.check_for_sect_clear():
                    self.controller.mode = "movement"
                    self.controller.combat_cooldown = time.time() + 5
                    break

                if self.dunchk_momentum < 20:
                    self.dunchk_momentum += 1
                if self.check_for_ongoing_combo():
                    pass
                elif self.check_for_enemies():
                    self.calc_nearest_enemy()
            elif self.dunchk_momentum >= 1:
                self.dunchk_momentum -= 1
            else:
                self.controller.mode = "movement"
                break
            # If loops are over 100fps, slow to 67fps
            if 100*(time.time() - loop_time) < 1:
                # Minimum sleep time is roughly 15ms regardless
                time.sleep(0.001)
            loop_time = time.time()
        self.running = False

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

    def check_for_sect_clear(self):
        # then try to detect the sect_clear
        sc_ss = self.sect_clear_wincap.get_screenshot()
        # pre-process the image to help with detection
        sect_clear_image = self.sect_clear_vision.apply_hsv_filter(
            sc_ss, self.sect_clear_filter)
        # do object detection, this time grab rectangles
        sect_clear_rectangles = self.sect_clear_vision.find(
            sect_clear_image, threshold=0.34, epsilon=0.5)
        # then return answer to whether sect clear is showing
        if len(sect_clear_rectangles) == 1:
            return True
        return False

    def check_for_ongoing_combo(self):
        # then try to detect the combo_count
        oc_ss = self.combo_count_wincap.get_screenshot()
        # pre-process the image to help with detection
        combo_count_image = self.combo_count_vision.apply_hsv_filter(
            oc_ss, self.combo_count_filter)
        # do object detection, this time grab rectangles
        combo_count_rectangles = self.combo_count_vision.find(
            combo_count_image, threshold=0.21, epsilon=0.5)
        # then return answer to whether currently in dungeon
        if len(combo_count_rectangles) >= 1:
            return True
        return False

    def calc_nearest_enemy(self):
        for x, y in self.enemy_locs:
            closest = 1000
            if x + y < closest:
                closest = x + y
                nearestx = x
                nearesty = y
        self.centre_mass_angle = self.calc_angle(
            nearestx, nearesty)
        # Then set the "target" enemy
        self.target_relative_coords = [nearestx, nearesty]

    def calc_angle(self, relx, rely):
        angle = math.degrees(math.atan2(rely, relx))
        if angle <= 90:
            angle = angle * -1 + 90
        else:
            angle = 360 + (angle-90) * -1
        return angle

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

    def point_at_target(self):
        if self.centre_mass_angle >= 315 or self.centre_mass_angle < 45:
            pydirectinput.keyDown("up")
        if self.centre_mass_angle >= 225 and self.centre_mass_angle < 315:
            pydirectinput.keyDown("left")
        if self.centre_mass_angle >= 135 and self.centre_mass_angle < 225:
            pydirectinput.keyDown("down")
        if self.centre_mass_angle >= 45 and self.centre_mass_angle < 135:
            pydirectinput.keyDown("right")

    def start_combo_handler(self):
        t = threading.Thread(target=self.combo_handler_MS)
        t.start()

    def combo_handler(self):
        if not self.running:
            self.running = True
            while self.running:
                if len(self.combo_queue) > 0:
                    key, duration = self.combo_queue[0]
                    nextkey = None
                    if len(self.combo_queue) > 1:
                        nextkey, _ = self.combo_queue[1]
                        if nextkey == "point":
                            # Need to point at centre mass of enemies or nearest in range enemy
                            self.point_at_target()
                    if key is None:
                        time.sleep(duration)
                    elif key == "move":
                        # Need to calculate time to press buttons in function
                        # And then press the required buttons
                        self.move_towards_target()
                    else:
                        pydirectinput.keyDown(key)
                        time.sleep(duration)
                        pydirectinput.keyUp(key)
                        time.sleep(0.07)
                    if nextkey == "point":
                        for key in ["up", "down", "left", "right"]:
                            pydirectinput.keyUp(key)
                    if len(self.combo_queue) > 0:
                        self.combo_queue.pop(0)
                    else:
                        print("Error, tried to pop when array was size 0")
                else:
                    self.combo_queue = self.combos.grab_preferred_combo().copy()
            else:
                self.combo_queue = []
                for key in ["up", "down", "left", "right"]:
                    pydirectinput.keyUp(key)

    def combo_handler_MS(self):
        if not self.running:
            self.running = True
            while self.running:
                if len(self.combo_queue) > 0:
                    key, duration = self.combo_queue[0]
                    nextkey = None
                    if len(self.combo_queue) > 1:
                        nextkey, _ = self.combo_queue[1]
                        if nextkey == "point":
                            # Need to point at centre mass of enemies or nearest in range enemy
                            self.point_at_target()
                    if key is None:
                        time.sleep(duration)
                    elif key == "move":
                        # Need to calculate time to press buttons in function
                        # And then press the required buttons
                        self.move_towards_target()
                    elif key == "moveplayer":
                        # Check if can find other player, then move towards
                        # But only for a specific duration
                        if self.can_find_other_player():
                            self.move_towards_other_player(duration)
                    elif key == "point":
                        pass
                    elif key == "x":
                        pydirectinput.keyDown(key)
                        time.sleep(duration)
                        pydirectinput.keyUp(key)
                        time.sleep(0.07)
                    elif key in self.cooldowns:
                        if time.time() > self.cd_tracker[key]:
                            self.cd_tracker[key] = time.time() + \
                                self.cooldowns[key]
                            pydirectinput.keyDown(key)
                            time.sleep(duration)
                            pydirectinput.keyUp(key)
                            time.sleep(0.07)
                        else:
                            # Grab the cooldowns of all available keys
                            # Check if any are ready yet, if yes then go next loop
                            if self.can_create_preferred_available_order():
                                pass
                            # If it isnt move towards the other player if detected
                            # And keep doing that until the next cooldown is up
                            elif self.can_find_other_player():
                                self.move_towards_other_player()
                            # Or else move opposite direction to enemies but stay in range
                            else:
                                self.move_towards_safety()
                    if nextkey == "point":
                        for key in ["up", "down", "left", "right"]:
                            pydirectinput.keyUp(key)
                else:
                    self.combo_queue = self.combos.grab_preferred_combo().copy()
            else:
                self.combo_queue = []
                self.remove_all_keypresses()

    def can_create_preferred_available_order(self):
        # This will check the current available keys
        # And if any are not on cooldown i.e. available to use
        # Will create a new order for the combo queue
        # Based on the preferred combo order
        available = []
        for key, cd_time in self.cd_tracker.items():
            if time.time > cd_time:
                available.append(key)
        if len(available) == 0:
            return False
        else:
            self.add_keys_to_queue(available, True)
            return True

    def add_keys_to_queue(self, available, overwrite=False):
        prioritised = []
        # First need to sort the keys in order of priority
        for key in self.combos.grab_preferred_order():
            if key in available:
                prioritised.append(key)
        # Overwrite if necessary
        if overwrite:
            self.combo_queue = []
        # Then add to combo queue
        for key in prioritised:
            self.combo_queue.append([key, 0.15])

    def move_towards_other_player(self):
        # This will move the current character towards the other player
        # Usually while waiting for cooldowns
        # Then do the movement towards other player
        self.move_towards_target(self.other_player_rel_coords)
        # If has taken more than enough time then all fine
        # Otherwise it will loop again and probably end up
        # back here again, not sure if this is an issue or not

    def move_towards_safety(self):
        # This will attempt to stay within range of average enemy position
        # But move away from them to hopefully dodge attacks
        # First grab the coords and get opposite
        movex = self.target_relative_coords[0]
        movey = self.target_relative_coords[1]
        abx = abs(movex)
        aby = abs(movey)
        # Then figure out how far to move to stay within range
        ratio = (abx + aby)/self.dist_threshold
        # Check if already too far away from target then move closer
        if ratio < 1:
            # If within range then move back to max range
            self.move_towards_target(
                [int((-movex/(abx+aby))*self.dist_threshold), int(-movey/(abx+aby)*self.dist_threshold)])
        else:
            # Move halfway towards the nearest enemy
            self.move_towards_target([int(movex/2), int(movey/2)])

    def add_move_next_action(self):
        # Only grab the first i.e. current action and remove the rest
        self.combo_queue = self.combo_queue[:1]
        # And then append the instruction to move afterwards
        self.combo_queue.append(["move", 2])

    def remove_all_keypresses(self):
        for key in ["up", "down", "left", "right"]:
            pydirectinput.keyUp(key)
        for key in ["a", "s", "d", "f", "g", "h"]:
            pydirectinput.keyUp(key)

    def move_towards_target(self, coords=False):
        # Default pixels/sec test move rate was 50pixels in 2.5sec minimap
        # Which is 20pixels/sec
        if coords:
            xdist_to_move = coords[0]
            ydist_to_move = coords[1]
        else:
            xdist_to_move = self.target_relative_coords[0]
            ydist_to_move = self.target_relative_coords[1]
        if xdist_to_move > 0:
            pydirectinput.keyDown("right")
        elif xdist_to_move < 0:
            pydirectinput.keyDown("left")
        if ydist_to_move > 0:
            pydirectinput.keyDown("up")
        elif ydist_to_move < 0:
            pydirectinput.keyDown("down")
        # Now hold the buttons until moved to target location
        xdist_to_move = abs(xdist_to_move)
        ydist_to_move = abs(ydist_to_move)
        counter = 0
        while self.running:
            time.sleep(0.1)
            counter += 1
            x_remain = xdist_to_move - 2*counter
            y_remain = ydist_to_move - 2*counter
            if x_remain <= 0:
                pydirectinput.keyUp("right")
                pydirectinput.keyUp("left")
            if y_remain <= 0:
                pydirectinput.keyUp("up")
                pydirectinput.keyUp("down")
            if x_remain <= 0 and y_remain <= 0:
                # Releasing keys to catch any bugs or errors here
                pydirectinput.keyUp("right")
                pydirectinput.keyUp("left")
                pydirectinput.keyUp("up")
                pydirectinput.keyUp("down")
                break
            if counter >= 80:
                pydirectinput.keyUp("right")
                pydirectinput.keyUp("left")
                pydirectinput.keyUp("up")
                pydirectinput.keyUp("down")
                break

    def initialise_wep_class(self):
        # First create the classes with required information
        if self.weapon == "MSU":
            self.combos = combo.MSUnfocused(level=self.level)
        elif self.weapon == "MSF":
            self.combos = combo.MSFocused(level=self.level)
        elif self.weapon == "WBU":
            self.combos = combo.WeaponBagUnfocused(level=self.level)
        elif self.weapon == "WBF":
            self.combos = combo.WeaponBagFocused(level=self.level)

        # Second figure out which keys to track cooldowns for
        for key, value in self.combos.grab_base_cooldowns().items():
            if value:
                self.cooldowns[key] = value
                self.cd_tracker[key] = time.time()
        self.cooldowns.pop("popthis")
        self.cd_tracker.pop("popthis")

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

    def get_monitor_scaling():
        user32 = ctypes.windll.user32
        w_orig = GetSystemMetrics(0)
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        return float(("{:.2f}".format(w/w_orig)))


if __name__ == "__main__":
    cs = StandaloneCombat(controller=None)
    time.sleep(2)
    cs.combat_mainloop()
