# This will be the file which handles the combat mode
# The keypresses themselves will be drawn from the combo file
# In particular the relevant weapon in the combo file
from hsvfilter import grab_object_preset
from windowcapture import WindowCapture
from vision import Vision
import os
import combo


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
        self.move_queue = []

        # Variables for keeping track of which skills are on cooldown
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
        self.sect_clear_vision = Vision('otherplayer67.jpg')

        # Initialised the combo object
        # Will have this choose the right object depending on weapon in future
        self.combobot = combo.WeaponBagUnfocused()

        self.run()

    def run(self):
        while self.running:
            # Need to check for section cleared message
            if self.check_for_sect_clear():
                break
            if self.check_for_enemies():
                # Need to figure out if have moves ongoing/remaining
                if len(self.move_queue) < 2:
                    self.move_queue = self.combobot.grab_preferred_combo()
                # Then carry out the combo until no detections
            elif len(self.move_queue) > 0:
                # Need to check to see if combo count still rising
                pass

    def stop(self):
        self.enabled = False

    def update_target(self):
        # This is for pointing character in correct direction
        # Want to always be pointed towards the bulk of the enemies
        pass

    def check_for_enemies(self):
        # Placeholder for now
        # Grab enemy positions
        self.mainloop.minimap_screenshot
        # Figure out if
        return False

    def check_for_sect_clear(self):
        # Placeholder for now
        return False
