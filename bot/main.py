import pydirectinput as pdi
import time


class RHBot():
    def __init__(self) -> None:
        pdi.FAILSAFE = True
        self.current_zone = 0

    def main(self, num_loops=10):
        # Main flow of bot
        # For a given number of loops, run through the dungeon
        loop_counter = 0
        while loop_counter < num_loops:
            while self.current_zone < 10:
                # To start => move to spawn the first enemies
                self.move_to_next_area(self.current_zone)
                # Then initiate combat
                self.perform_combat()
                # Once no more enemies left
            # Then once the dungeon/level has been completed, perform level end tasks
            self.level_end_sequence()
            loop_counter += 1

    def move_to_next_area(self):
        if self.current_zone == 0:
            pass
        pass

    def perform_combat(self):
        enemies_detected = True
        while enemies_detected:
            enemies_detected = False
        # Do something

    def level_end_sequence(self):
        pass

    def detect_map_objects(self):
        pass


if __name__ == "__main__":
    rhb = RHBot()
    rhb.main()
