import pydirectinput as pdi
import time
import os
import json
import numpy as np


class RHBot():
    def __init__(self) -> None:
        pdi.FAILSAFE = True
        # The variable that will keep track of the zones
        self.current_zone = 0
        # The variable that will estimate from the map the current position
        # Used for checking if within attacking distance
        # And also used for calculating what buttons to press to travel to the next area
        self.current_pos = {0, 0}

        # These will hold the current skill cooldown finish times
        self.cooldown_end_time = {
            "a": 0, "b": 0, "d": 0, "f": 0, "g": 0, "h": 0
        }

    def main(self, num_loops=10):
        # Main flow of bot
        # For a given number of loops, run through the dungeon
        loop_counter = 0
        while loop_counter < num_loops:
            while self.current_zone < 10:
                # To start => move to spawn the first enemies
                self.move_to_next_area(self.current_zone)
                # Then initiate combat
                self.begin_combat()
                # Once no more enemies left
            # Then once the dungeon/level has been completed, perform level end tasks
            self.level_end_sequence()
            loop_counter += 1
            if loop_counter < num_loops:
                self.start_new_level()
            else:
                # For now will just print finished and leave it at that
                print("Finished {} loops".format(num_loops))

    def move_to_next_area(self):
        if self.current_zone == 0:
            pass
        pass

    def begin_combat(self):
        enemies_detected = True
        while enemies_detected:
            # Find what needs to be targeted (or move closer)
            self.calc_enemies_to_target()
            # Perform attacks based on available skills/cooldowns
            self.perform_attacks()
            # Finally check if there are any enemies remaining
            enemies_detected = self.detect_enemies()
        # Do something

    def perform_attacks():
        pass

    def calc_enemies_to_target(self):
        # Check for priority enemies

        # The check if need to move closer to (priority) enemies
        pass

    def level_end_sequence(self):
        pass

    def detect_enemies(self):
        return False

    def detect_map_objects(self):
        pass

    def start_new_level(self):
        # Press the requires buttons to start a new level

        # Then detect objects of interest when the map spawns in
        self.detect_map_objects()

    def pick_up_loot(self):
        pass


if __name__ == "__main__":
    rhb = RHBot()
    rhb.main()
