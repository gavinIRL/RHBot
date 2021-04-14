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
        # Calculate the centre mass angle if multiple enemies
        self.centre_mass_angle = 90
        # If up against boss, will move less
        self.boss_fight = False
        # Flag to say if there is an ongoing combo counter or not
        self.ongoing_combo_count = False
        self.frames_since_combo_detect = 1000
        # Variable to say if other player detected recently
        self.ongoing_other_player_visible = False

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
            # To do: incorporate a dungeon check
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
            elif len(self.combo_queue) > 0:
                if self.check_for_ongoing_combo():
                    self.frames_since_combo_detect = 0
                else:
                    do_enemy_check = True
            # Otherwise need to see where enemies are on map
            # And move towards them
            elif self.check_for_enemies():
                # Need to calculate how far the nearest enemy is
                # From that calculate a travel time to get into range if required
                # And then add a move command to the combo queue
                # And reassess all moves after the move command
                pass

    def stop(self):
        self.enabled = False

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
        pass

    def check_for_enemies(self):
        # Placeholder for now
        # Grab enemy positions
        self.mainloop.minimap_screenshot
        # If more than 3 detections then aim centre mass
        # Otherwise calculate the closest enemy and aim at that
        return False

    def check_for_sect_clear(self):
        # Placeholder for now
        return False

    def check_for_ongoing_combo(self):
        pass

    def start_combo(self):
        while self.running:
            if len(self.combo_queue) > 0:
                key, duration = self.combo_queue[0]
                if key is None:
                    time.sleep(duration)
                elif key == "move":
                    # First check if there is an ongoing combo
                    if self.ongoing_combo_count:
                        pass
                    # Otherwise need to move closer to the other player
                    elif self.ongoing_other_player_visible:
                        pass
                    # Otherwise move towards centre mass of enemies
                    pass
                elif key == "point":
                    # Need to point at centre mass of enemies or nearest in range enemy
                    pass
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
