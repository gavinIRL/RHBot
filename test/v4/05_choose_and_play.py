# This file will allow the user to quickly choose
# an action-sequence to play and then carry out the action sequence
# It will wait in the background until a certain key is pressed
# and then it will perform another action
from pynput.keyboard import Key, Listener, KeyCode
import time
import os


class TestController():
    def __init__(self, loot=True, combat=True, freemove=False) -> None:
        self.mode = "movement"
        self.listener = None
        self.bot_running = False
        self.loot_enabled = loot
        self.combat_enabled = combat
        self.freemove_enabled = freemove
        self.playback_flag = False
        self.playback_string = ""

    def start_keypress_listener(self):
        if self.listener == None:
            self.listener = Listener(on_press=self.on_press,
                                     on_release=self.on_release)
            self.listener.start()

    def on_press(self, key):
        if key == KeyCode(char='t'):
            self.playback_flag = not self.playback_flag
            if self.playback_flag:
                self.playback_string = ""
                print("Select a recording number")
            else:
                # To-do: Start the playback
                print("Starting recording number "+self.playback_string)
                pass
        elif self.playback_flag:
            # add the key to existing string
            self.playback_string += str(key)
        else:
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
            # self.combatbat.running = False
            # Need to pause for 1 second and then clear all keypresses
            time.sleep(0.5)
            # self.combatbat.remove_all_keypresses()
            print("Exiting bot")
            os._exit(1)
