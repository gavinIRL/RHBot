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
    def __init__(self, main, weapon="WB") -> None:
        # Change the working directory to the folder this script is in.
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # Variable to turn combat on/off from main loop

        # Variable to determine which combos to use
        self.weapon = weapon
        # Variable for storing mainloop object
        self.mainloop = main
        # List for storing actions to carry out
        # Format of each entry will be as follows:
        # button or none, length of action
        self.combo_queue = []
        # This variable will change combat behaviour
        # If nearest enemy distance is too big, will move towards them
        self.nearest_enemy_dist = 1
        self.dist_threshold = 125  # To-do: update this value based on testing
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
        # Variable to determine if there is already a move thread in progress
        self.move_thread_running = False

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

    def begin(self):

        # Grab the gamename from the text file
        with open("gamename.txt") as f:
            gamename = f.readline()

        # The next block of code is setup for detecting the section cleared msg
        self.sect_clear_filter, sect_clear_custom_rect = grab_object_preset(
            sect_clear_name="message_section_cleared")
        # initialize the WindowCapture class for sect_clear detection
        self.sect_clear_wincap = WindowCapture(
            gamename, sect_clear_custom_rect)
        # initialize the Vision class
        self.sect_clear_vision = Vision('SectionCleared67.jpg')

        # The next block of code is setup for detecting the combo count
        self.combo_count_filter, combo_count_custom_rect = grab_object_preset(
            combo_count_name="combo_count")
        # initialize the WindowCapture class for combo_count detection
        self.combo_count_wincap = WindowCapture(
            gamename, combo_count_custom_rect)
        # initialize the Vision class
        self.combo_count_vision = Vision('combocount67.jpg')
        # And finally run the actual bot
        # self.start()

    def start_combat_bot(self):
        print("Got to combat start")
        # Need to start off by pointing in the right direction
        self.point_at_target()
        self.dunchk_momentum = 20

        # Initialise the combo object
        # Will have this choose the right object depending on weapon in future
        self.combos = combo.WeaponBagFocused()

        # This will start a separate thread for the combo actions
        if not self.move_thread_running:
            t = threading.Thread(target=self.start_combo, daemon=True)
            t.start()
            self.move_thread_running = True
        self.maincombatloop()

    def maincombatloop(self):
        # self.mainloop.combat_running[0] = 1
        currplayer_counter = 0
        while self.mainloop.combat_running[0] == 1:
            # print("Another combat loop")
            currplayer_counter += 1
            if self.mainloop.check_if_in_dungeon():
                print("Did a successful dungeon check")
                self.combo_running = True
                if self.dunchk_momentum < 60:
                    self.dunchk_momentum += 120
                self.frames_since_combo_detect += 1
                do_enemy_check = False
                # Need to check for section cleared message
                if self.check_for_sect_clear():
                    # Tell the main loop the section is clear
                    self.stop()
                    break
                # Otherwise if combo detected in either of previous
                # 2 frames then check again rather than enemy checking
                elif self.frames_since_combo_detect <= 2:
                    if self.check_for_ongoing_combo():
                        print("Detected a combo")
                        self.frames_since_combo_detect = 0
                # Otherwise special handling for boss fight
                # elif self.boss_fight:
                #     do_enemy_check = True
                #     pass
                # If not in boss fight and performing moves then check for combo
                # this only occurs when no combo detected in a while
                elif len(self.combo_queue) > 0:
                    if self.check_for_ongoing_combo():
                        self.frames_since_combo_detect = 0
                        print("Detected a combo #2")
                    else:
                        do_enemy_check = True
                        print("Detected a combo #3")
                # Otherwise need to see where enemies are on map
                # And move towards them
                elif do_enemy_check:
                    if not self.check_for_enemies():
                        if self.dunchk_momentum >= 2:
                            self.dunchk_momentum -= 2
                        else:
                            print("Exited due to #3")
                            self.stop()
                            break
                # Need to figure out if this is redundant
                else:
                    if self.dunchk_momentum >= 1:
                        self.dunchk_momentum -= 1
                    else:
                        print("Exited due to momentum #1")
                        self.stop()
                        break
            elif self.dunchk_momentum >= 1:
                self.dunchk_momentum -= 1
            else:
                # Need a handler for exiting combat mode here
                print("Exited due to #2")
                self.stop()
            if currplayer_counter >= 4:
                self.mainloop.can_find_current_player()
                self.mainloop.can_find_other_player()
                currplayer_counter = 0
        else:
            print("Exited due to #4 - after while")
            self.stop()

    def stop(self):
        self.mainloop.combat_running[0] = 0
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
        for key in ["up", "down", "left", "right"]:
            pydirectinput.keyUp(key)
        # This is for pointing character in correct direction
        # Want to always be pointed towards the bulk of the enemies

    def check_for_enemies(self):
        # Placeholder for now
        # Grab enemy positions
        self.mainloop.minimap_screenshot = self.mainloop.minimap_wincap.get_screenshot()
        # pre-process the image to help with detection
        enemy_output_image = self.mainloop.enemy_minimap_vision.apply_hsv_filter(
            self.mainloop.minimap_screenshot, self.mainloop.enemy_minimap_filter)
        # do object detection, this time grab points
        enemy_rectangles = self.mainloop.enemy_minimap_vision.find(
            enemy_output_image, threshold=0.45, epsilon=0.5)
        # then return answer to whether enemies are detected
        if len(enemy_rectangles) >= 1:
            # grab points
            points = self.mainloop.enemy_minimap_vision.get_click_points(
                enemy_rectangles)
            points = self.get_relative_to_player(points)
            # To-do: translate to relative position vs player
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
                # Move closer based on distance, aim to get within 50px
                if abs(int(nearestx*0.6)) <= 50:
                    self.target_relative_coords[0] = int(nearestx*0.6)
                else:
                    if nearestx > 0:
                        self.target_relative_coords[0] = nearestx - 50
                    else:
                        self.target_relative_coords[0] = nearestx + 50
                if abs(int(nearesty*0.6)) <= 50:
                    self.target_relative_coords[1] = int(nearesty*0.6)
                else:
                    if nearesty > 0:
                        self.target_relative_coords[1] = nearesty - 50
                    else:
                        self.target_relative_coords[1] = nearesty + 50
                self.add_move_next_action()

            return True
        else:
            # Change the target to be the other player
            if self.mainloop.can_find_other_player():
                self.target_relative_coords[0] = self.mainloop.other_player_rel_coords[0]
                self.target_relative_coords[1] = self.mainloop.other_player_rel_coords[1]
            else:
                # Just go with the most recent target I guess? Test this
                pass
        return False

    def check_for_sect_clear(self):
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

    def check_for_ongoing_combo(self):
        # then try to detect the combo_count
        ss = self.combo_count_wincap.get_screenshot()
        # pre-process the image to help with detection
        combo_count_image = self.combo_count_vision.apply_hsv_filter(
            ss, self.combo_count_filter)
        # do object detection, this time grab rectangles
        combo_count_rectangles = self.combo_count_vision.find(
            combo_count_image, threshold=0.21, epsilon=0.5)
        # then return answer to whether currently in dungeon
        if len(combo_count_rectangles) == 1:
            return True
        return False

    def start_combo(self):
        while self.mainloop.combat_running[0] == 1:
            # Need to catch waiting for detections to happen
            # Caused by asyncronous threading
            if not self.combo_running:
                time.sleep(0.2)
            elif len(self.combo_queue) > 0:
                # print(self.combo_queue[0])
                key, duration = self.combo_queue[0]
                if key is None:
                    time.sleep(duration)
                elif key == "move":
                    # Need to calculate time to press buttons in function
                    # And then press the required buttons
                    print("At move call data is: angle={}".format(
                        self.centre_mass_angle))
                    self.move_towards_target()
                elif key == "point":
                    # Need to point at centre mass of enemies or nearest in range enemy
                    print("At point call data is: angle={}".format(
                        self.centre_mass_angle))
                    self.point_at_target()
                else:
                    pydirectinput.keyDown(key)
                    time.sleep(duration)
                    pydirectinput.keyUp(key)
                    time.sleep(0.05)
                self.combo_queue.pop(0)
            else:
                self.combo_queue = self.combos.grab_preferred_combo().copy()
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
        # print("Angle calc: x={}, y={}, angle={}".format(relx, rely, angle))
        return angle

    def add_move_next_action(self):
        # Only grab the first i.e. current action and remove the rest
        self.combo_queue = self.combo_queue[:1]
        # And then append the instruction to move afterwards
        self.combo_queue.append(["move", 2])

    def move_towards_target(self):
        self.move_thread_running = True
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
        while self.mainloop.combat_running[0] == 1:
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
                # Releasin keys to catch any bugs or errors here
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
        self.move_thread_running = False
