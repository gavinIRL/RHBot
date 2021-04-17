# This will be the file which handles the combat mode
# The keypresses themselves will be drawn from the combo file
# In particular the relevant weapon in the combo file
from hsvfilter import grab_object_preset
from windowcapture import WindowCapture
from vision import Vision
import os
import combo
import threading
import time
import pydirectinput
import math


class Combat():
    def __init__(self, main, combat_running, weapon="WB") -> None:
        # Change the working directory to the folder this script is in.
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # Variable to turn combat on/off from main loop
        self.running = combat_running
        # Variable to determine which combos to use
        self.weapon = weapon
        # Variable for storing mainloop object
        self.mainloop = main
        # List for storing actions to carry out
        # Format of each entry will be as follows:
        # button or none, length of action
        self.combo_queue = []
        # Cooldown on combat to reduce false positive rate
        self.combat_cooldown = 0
        # This variable will change combat behaviour
        # If nearest enemy distance is too big, will move towards them
        self.nearest_enemy_dist = 1
        self.dist_threshold = 80  # To-do: update this value based on testing
        # Calculate the centre mass angle if multiple enemies
        self.centre_mass_angle = 90
        # If up against boss, will move less
        self.boss_fight = False
        # Flag to say if there is an ongoing combo counter or not
        self.ongoing_combo_count = False
        self.frames_since_combo_detect = 1000
        # Variable to say if other player detected recently
        self.ongoing_other_player_visible = False
        # Momentum variables for dunchk
        self.dunchk_momentum = 0
        # Variable to prevent combo starting prior to mainloop
        self.combo_running = False
        # Veriable to store target relative position (nearest enemy, player)
        self.target_relative_coords = [0, 0]

        # Variables for keeping track of which skills are on cooldown
        # The numbers will correspond to time at which off cooldown next
        # Basic asdfgh skills up first
        self.cd_a = 0
        self.cd_s = 0
        self.cd_d = 0
        self.cd_f = 0
        self.cd_g = 0
        self.cd_h = 0
        # Then the shift + asdfgh skills
        self.cd_sa = 0
        self.cd_ss = 0
        self.cd_sd = 0
        self.cd_sf = 0
        self.cd_sg = 0
        self.cd_sh = 0
        # Then the buff skills
        self.cd_f1 = 0
        self.cd_f2 = 0
        self.cd_f3 = 0
        self.cd_f4 = 0

    def update_cooldowns(self):
        pass

    def start(self):

        # The next block of code is setup for detecting enemies on minimap
        # This uses same image as player minimap in mainloop
        self.enemy_minimap_filter, _ = grab_object_preset(
            enemy_minimap_name="enemy_map_locv3")
        # initialize the Vision class
        self.enemy_minimap_vision = Vision('enemy67.jpg')

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

        # Need to start off by pointing in the right direction
        # Todo: replace/remove the first call as initial reason to enter
        # combat mode will provide required information to point
        self.check_for_enemies()
        self.point_at_target()

        # Initialise the combo object
        # Will have this choose the right object depending on weapon in future
        self.combos = combo.WeaponBagUnfocused()

        # This will start a separate thread for the combo actions
        t = threading.Thread(target=self.start_combo, daemon=True)
        t.start()
        # And finally run the actual bot
        self.run()

    def run(self):
        while self.running:
            if self.mainloop.check_if_in_dungeon():
                self.combo_running = True
                if self.dunchk_momentum < 4:
                    self.dunchk_momentum += 1
                self.frames_since_combo_detect += 1
                do_enemy_check = False
                # Need to check for section cleared message
                if self.check_for_sect_clear():
                    # Put the combat bot on cooldown
                    self.combat_cooldown = time.time() + 2
                    # Tell the main loop the section is clear

                    # And then break out of the loop
                    # Using a method instead of break for clarity
                    self.stop()
                # Otherwise if combo detected in either of previous
                # 4 frames then check again rather than enemy checking
                elif self.frames_since_combo_detect <= 4:
                    if self.check_for_ongoing_combo():
                        self.frames_since_combo_detect = 0
                # Otherwise special handling for boss fight
                elif self.boss_fight:
                    # If can detect other player move towards

                    # Otherwise do an enemy map check
                    pass
                # If not in boss fight and performing moves then check for combo
                # this only occurs when no combo detected in a while
                elif len(self.combo_queue) > 0:
                    if self.check_for_ongoing_combo():
                        self.frames_since_combo_detect = 0
                    else:
                        do_enemy_check = True
                # Otherwise need to see where enemies are on map
                # And move towards them
                elif do_enemy_check:
                    if self.check_for_enemies():
                        pass
                        # Need to calculate how far the nearest enemy is
                        # From that calculate a travel time to get into range if required
                        # And then add a move command to the combo queue
                        # And reassess all moves after the move command
                    else:
                        if self.dunchk_momentum >= 2:
                            self.dunchk_momentum -= 2
                        else:
                            self.stop()
                # Need to figure out if this is redundant
                else:
                    if self.dunchk_momentum >= 1:
                        self.dunchk_momentum -= 1
                    else:
                        self.stop()
                # Todo exit combat mode as a failsafe if don't detect enemies for a while
                # Or at least revert to loot mode with a frequent enemy check
                # Need a handler if don't detect enemies for a while
            elif self.dunchk_momentum >= 1:
                self.dunchk_momentum -= 1
            else:
                # Need a handler for exiting combat mode here
                self.stop()

    def stop(self):
        self.enabled = False
        self.combo_running = False

    def point_at_target(self):
        if self.centre_mass_angle >= 300 or self.centre_mass_angle <= 60:
            pydirectinput.keyDown("up")
        if self.centre_mass_angle >= 210 and self.centre_mass_angle <= 330:
            pydirectinput.keyDown("left")
        if self.centre_mass_angle >= 120 and self.centre_mass_angle <= 240:
            pydirectinput.keyDown("down")
        if self.centre_mass_angle >= 30 and self.centre_mass_angle <= 150:
            pydirectinput.keyDown("right")
        time.sleep(0.05)
        for key in ["up", "down", "left", "right"]:
            pydirectinput.keyUp(key)
        # This is for pointing character in correct direction
        # Want to always be pointed towards the bulk of the enemies

    def check_for_enemies(self):
        # Placeholder for now
        # Grab enemy positions
        self.mainloop.minimap_screenshot = self.mainloop.minimap_wincap.get_screenshot()
        # pre-process the image to help with detection
        enemy_output_image = self.enemy_minimap_vision.apply_hsv_filter(
            self.mainloop.minimap_screenshot, self.enemy_minimap_filter)
        # do object detection, this time grab points
        enemy_rectangles = self.enemy_minimap_vision.find(
            enemy_output_image, threshold=0.45, epsilon=0.5)
        # then return answer to whether enemies are detected
        if len(enemy_rectangles) >= 1:
            # grab points
            points = self.enemy_minimap_vision.get_click_points(
                enemy_rectangles)
            points = self.get_relative_to_player(points)
            # To-do: translate to relative position vs player
            if len(points) > 3:
                closest = 1000
                avgx = 0
                avgy = 0
                for x, y in points:
                    if x + y < closest:
                        closest = x + y
                        nearestx = x
                        nearesty = y
                    avgx += x
                    avgy += y
                avgx = avgx / len(points)
                avgy = avgy / len(points)
                self.centre_mass_angle = self.grab_angle(
                    nearestx, nearesty)
                # check if they are close enough
                if closest > self.dist_threshold:
                    # Move closer based on distance
                    self.add_move_next_action()
            else:
                # figure out closest enemy
                for x, y in points:
                    if x + y < closest:
                        closest = x + y
                        nearestx = x
                        nearesty = y
                self.centre_mass_angle = self.grab_angle(
                    nearestx, nearesty)
                # Then figure out if need to move closer
                if closest > self.dist_threshold:
                    # Move closer based on distance
                    self.add_move_next_action()
            return True
        return False

    def check_for_sect_clear(self):
        # Placeholder for now
        return False

    def check_for_ongoing_combo(self):
        # then try to detect the sect_clear
        ss = self.sect_clear_wincap.get_screenshot()
        # pre-process the image to help with detection
        sect_clear_image = self.sect_clear_vision.apply_hsv_filter(
            ss, self.sect_clear_filter)
        # do object detection, this time grab rectangles
        sect_clear_rectangles = self.sect_clear_vision.find(
            sect_clear_image, threshold=0.34, epsilon=0.5)
        # then return answer to whether currently in dungeon
        if len(sect_clear_rectangles) == 1:
            return True
        return False

    def start_combo(self):
        while self.running:
            # Need to catch waiting for detections to happen
            # Caused by asyncronous threading
            if not self.combo_running:
                time.sleep(0.2)
            elif len(self.combo_queue) > 0:
                key, duration = self.combo_queue[0]
                if key is None:
                    time.sleep(duration)
                elif key == "move":
                    # Need to calculate time to press buttons in function
                    # And then press the required buttons
                    self.move_towards_target()
                elif key == "point":
                    # Need to point at centre mass of enemies or nearest in range enemy
                    self.point_at_target()
                else:
                    pydirectinput.keyDown(key)
                    time.sleep(duration)
                    pydirectinput.keyUp(key)
                    time.sleep(0.05)
                self.combo_queue.pop(0)
            else:
                self.combo_queue.append(self.combos.grab_preferred_combo())
        else:
            self.combo_queue = []

    def get_relative_to_player(self, abs_list):
        # This will convert the points in a list
        # To be relative to the player
        playerx = self.mainloop.current_player_coords[0]
        playery = self.mainloop.current_player_coords[1]
        returnlist = []
        for x, y in abs_list:
            relx = x - playerx
            rely = playery - y
            returnlist.append([relx, rely])
        return returnlist

    def grab_angle(self, relx, rely):
        angle = math.degrees(math.atan2(rely, relx))
        if angle <= 90:
            angle = angle * -1 + 90
        else:
            angle = 360 + (angle-90) * -1
        return angle

    def add_move_next_action(self):
        # Only grab the first i.e. current action and remove the rest
        self.combo_queue = self.combo_queue[:1]
        # And then append the instruction to move afterwards
        self.combo_queue.append(["move", 2])

    def move_towards_target(self):
        # Default pixels/sec test move rate was 50pixels in 2.5sec minimap
        # Which is 20pixels/sec
        xdist_to_move = self.target_relative_coords[0]
        ydist_to_move = self.target_relative_coords[0]
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
        while True:
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
                break
