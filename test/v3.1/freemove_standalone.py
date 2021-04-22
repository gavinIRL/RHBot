# This file will allow the user to freely move the character
# But once an enemy is detected it will swap to combat mode
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import grab_object_preset
import os
import time


class StandaloneFreeMove():
    def __init__(self, controller) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.controller = controller
        self.enemy_detect_frames = 0

        # The next block of code is setup for detecting enemies on minimap
        self.enemy_filter, enemy_custom_rect = grab_object_preset(
            object_name="enemy_map_locv3")
        self.enemy_wincap = WindowCapture(
            "Rusty Hearts: Revolution - Reborn ", enemy_custom_rect)
        self.enemy_vision = Vision('enemy67.jpg')

    def freemove_mainloop(self):
        # print("Entering freemove")
        loop_time = time.time()
        while self.controller.bot_running:
            # Will attempt to detect enemies, if so will enter combat mode
            # Only exception would be if combat is disabled
            # In which case the bot will just sleep
            if self.controller.combat_enabled:
                if self.perform_enemy_check():
                    if (time.time() - self.controller.combat_cooldown) > 0:
                        self.controller.mode = "combat"
                        # print("Entering automated combat")
                        break
            else:
                time.sleep(0.25)
            # If loops are over 100fps, slow to 67fps
            if 100*(time.time() - loop_time) < 1:
                # Minimum sleep time is roughly 15ms regardless
                time.sleep(0.001)
            loop_time = time.time()
            if not self.controller.freemove_enabled:
                print("Returning to automatic navigation")
                break

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
