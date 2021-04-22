# This will be the main file that will alternate between
# movement and combat modes as needs be
# It will check every 100ms if a module requires starting
import time
import os
from combat_standalone import StandaloneCombat
from moveloot_standalone import StandaloneMoveLoot
from freemove_standalone import StandaloneFreeMove
from pynput.keyboard import Key, Listener, KeyCode

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Controller():
    def __init__(self, loot=True, combat=True, freemove=False) -> None:
        self.mode = "movement"
        self.listener = None
        self.bot_running = False
        self.loot_enabled = loot
        self.combat_enabled = combat
        self.freemove_enabled = freemove
        self.movebot = StandaloneMoveLoot(self)
        self.combatbat = StandaloneCombat(self)
        self.freemovebot = StandaloneFreeMove(self)
        self.combat_cooldown = 0

    def start_controller(self):
        self.start_countdown()
        self.start_keypress_listener()
        while self.bot_running:
            time.sleep(0.01)
            if self.mode == "movement":
                if not self.freemove_enabled:
                    self.movebot.move_mainloop()
                else:
                    self.freemovebot.freemove_mainloop()
            elif self.mode == "combat":
                if (time.time() - self.combat_cooldown) > 0:
                    self.combatbat.combat_mainloop()
            else:
                print("Error, no mode selected")
                time.sleep(2)
        # print("Finished controller mainloop")
        # self.listener.

    def start_keypress_listener(self):
        if self.listener == None:
            self.listener = Listener(on_press=self.on_press,
                                     on_release=self.on_release)
            self.listener.start()

    def on_press(self, key):
        # print(str(key))
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
        if key == KeyCode(char='r'):
            self.freemove_enabled = not self.freemove_enabled
            if self.freemove_enabled:
                print("FREEMOVE ON")
            else:
                print("FREEMOVE OFF")

    def on_release(self, key):
        if key == KeyCode(char='q'):
            self.bot_running = False
            self.combatbat.running = False
            # Need to pause for 1 second and then clear all keypresses
            time.sleep(0.5)
            self.combatbat.remove_all_keypresses()
            print("Exiting bot")
            os._exit(1)

    def start_countdown(self):
        print("Bot starting in 3 seconds")
        time.sleep(1)
        print("Bot starting in 2 seconds")
        time.sleep(1)
        print("Bot starting in 1 seconds")
        time.sleep(1)
        self.bot_running = True


if __name__ == "__main__":
    cont = Controller(freemove=True)
    cont.start_controller()
