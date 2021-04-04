# This is to figure out what does and doesn't work in the game
# Having issues where nothing is being sent to the game
import pyautogui
import pydirectinput
import time
from threading import Thread, Lock


class Movement_Handler():
    def __init__(self, test_mode=False) -> None:
        self.stopped = True  # This refers to the thread
        self.lock = Lock()
        self.relx = 0
        self.rely = 0
        self.pressed_keys = []
        self.test_mode = test_mode

    def movement_start(self):
        self.stopped = False
        t = Thread(target=self.movement_run)
        t.start()

    def movement_stop(self):
        self.stopped = True

    def movement_run(self):
        while not self.stopped:
            if self.relx > 0:
                # Check if opposite key held down
                if "left" in self.pressed_keys:
                    self.pressed_keys.remove("left")
                    if not self.test_mode:
                        pydirectinput.keyUp("left")
                # Check that not already being held down
                if "right" not in self.pressed_keys:
                    self.pressed_keys.append("right")
                    # Hold the key down
                    if not self.test_mode:
                        pydirectinput.keyDown("right")
                    else:
                        print("Pressing right key")
            elif self.relx < 0:
                # Check if opposite key held down
                if "right" in self.pressed_keys:
                    self.pressed_keys.remove("right")
                    if not self.test_mode:
                        pydirectinput.keyUp("right")
                # Check that not already being held down
                if "left" not in self.pressed_keys:
                    self.pressed_keys.append("left")
                    # Hold the key down
                    if not self.test_mode:
                        pydirectinput.keyDown("left")
                    else:
                        print("Pressing left key")
            else:
                # Handling for case where = 0, need to remove both keys
                if "right" in self.pressed_keys:
                    self.pressed_keys.remove("right")
                    if not self.test_mode:
                        pydirectinput.keyUp("right")
                if "left" in self.pressed_keys:
                    self.pressed_keys.remove("left")
                    if not self.test_mode:
                        pydirectinput.keyUp("left")

            # Handling for y-dir next
            if self.rely > 0:
                # Check if opposite key held down
                if "down" in self.pressed_keys:
                    self.pressed_keys.remove("down")
                    if not self.test_mode:
                        pydirectinput.keyUp("down")
                # Check that not already being held down
                if "up" not in self.pressed_keys:
                    self.pressed_keys.append("up")
                    # Hold the key down
                    if not self.test_mode:
                        pydirectinput.keyDown("up")
                    else:
                        print("Pressing up key")
            elif self.rely < 0:
                # Check if opposite key held down
                if "up" in self.pressed_keys:
                    self.pressed_keys.remove("up")
                    if not self.test_mode:
                        pydirectinput.keyUp("up")
                # Check that not already being held down
                if "down" not in self.pressed_keys:
                    self.pressed_keys.append("down")
                    # Hold the key down
                    if not self.test_mode:
                        pydirectinput.keyDown("down")
                    else:
                        print("Pressing down key")
            else:
                # Handling for case where = 0, need to remove both keys
                if "up" in self.pressed_keys:
                    self.pressed_keys.remove("up")
                    if not self.test_mode:
                        pydirectinput.keyUp("up")
                if "down" in self.pressed_keys:
                    self.pressed_keys.remove("down")
                    if not self.test_mode:
                        pydirectinput.keyUp("down")
        # Stop pressing all keys if stopped
        else:
            for key in self.pressed_keys:
                self.pressed_keys.remove(key)
                pydirectinput.keyUp(key)

    def movement_update_xy(self, relx, rely):
        self.lock.acquire()
        self.relx = relx
        self.rely = rely
        self.lock.release()
