import pyautogui as pag
from time import sleep, time


class Actions():
    def __init__(self) -> None:
        self.pressed_keys = []
        self.start_time = time()

    def move_direction(self, relx, rely):
        if relx > 0:
            # Check if left key held down
            if "left" in self.pressed_keys:
                self.pressed_keys.remove("left")
            # Check that not already being held down
            if "right" not in self.pressed_keys:
                self.pressed_keys.append("right")
                # Hold the right key down
                pag.keyDown("right")

    def click(self, x, y):
        pass

    def elapsed_time(self):
        return time()-self.start_time
