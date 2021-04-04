# This is to figure out what does and doesn't work in the game
# Having issues where nothing is being sent to the game
import pyautogui
import pydirectinput
import time
from threading import Thread, Lock


class Movement_Handler():
    def __init__(self) -> None:
        self.stopped = True  # This refers to the thread
        self.lock = Lock()
        self.relx = 0
        self.rely = 0

    def movement_start(self):
        self.stopped = False
        t = Thread(target=self.movement_run)
        t.start()

    def movement_stop(self):
        self.stopped = True

    def movement_run(self):
        while not self.stopped:
            pass

    def movement_update_xy(self, relx, rely):
        self.lock.acquire()
        self.relx = relx
        self.rely = rely
        self.lock.release()
