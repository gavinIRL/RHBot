import cv2 as cv
import os
from time import time, sleep
import numpy as np
from pynput.keyboard import Key, Listener, KeyCode

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class HotkeyTest():
    def __init__(self) -> None:
        self.random_counter = 0
        self.looting_enabled = True
        self.bot_running = False

    def start(self):
        self.start_keypress_listener()

    def mainloop(self):
        while True:
            self.random_counter += 1
            print("Counter = {}".format(self.random_counter))
            sleep(0.5)

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
            self.looting_enabled = not self.looting_enabled
            print("Looting has been set to {}".format(self.looting_enabled))
        if key == KeyCode(char='e'):
            self.random_counter -= 10

    def on_release(self, key):
        # Do nothing
        pass
