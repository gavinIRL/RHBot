# This will be the main file that will alternate between
# movement and combat modes as needs be
# It will check every 100ms if a module requires starting
import time


class Controller():
    def __init__(self, loot=True, combat=True) -> None:
        self.mode = "movement"
        self.loot_enabled = loot
        self.combat_enabled = combat
        self.movebot = None
        self.combatbat = None

    def start_controller(self):
        previous = self.mode
        while True:
            time.sleep(0.1)
            if not previous == self.mode:
                if self.mode == "movement":
                    pass
                elif self.mode == "combat":
                    pass
