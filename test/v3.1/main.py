# This will be the main file that will alternate between
# movement and combat modes as needs be
# It will check every 100ms if a module requires starting
import time
import os
from combat_standalone import StandaloneCombat
from moveloot_standalone import StandaloneMoveLoot
from pynput.keyboard import Key, Listener, KeyCode

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Controller():
    def __init__(self, loot=True, combat=True) -> None:
        self.mode = "movement"
        self.listener = None
        self.bot_running = False
        self.loot_enabled = loot
        self.combat_enabled = combat
        self.movebot = StandaloneMoveLoot(self)
        self.combatbat = StandaloneCombat(self)

    def start_controller(self):
        self.bot_running = True
        while True:
            time.sleep(0.01)
            if self.mode == "movement":
                self.movebot.move_mainloop()
            elif self.mode == "combat":
                self.combatbat.combat_mainloop()
            else:
                print("Error, no mode selected")
                time.sleep(2)

    def start_keypress_listener(self):
        if self.listener == None:
            self.listener = Listener(on_press=self.on_press,
                                     on_release=self.on_release, suppress=True)
            self.listener.start()

    def on_press(self, key):
        if key == KeyCode(char='q'):
            self.bot_running = False
            return False
        if key == KeyCode(char='w'):
            self.loot_enabled = not self.loot_enabled
            if self.loot_enabled:
                print("LOOT ON")
            else:
                print("LOOT OFF")
        if key == KeyCode(char='e'):
            self.combat_enabled = not self.combat_enabled
            if self.combat_enabled:
                print("COMBAT ON")
            else:
                print("COMBAT OFF")

    def on_release(self, key):
        # Do nothing
        pass
