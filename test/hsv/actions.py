import pyautogui as pag
from time import sleep, time


class Actions():
    def __init__(self, test_mode=False) -> None:
        self.pressed_keys = []
        self.test_mode = test_mode

    def move_direction(self, relx, rely):
        # Handling for x-dir first
        # Making this verbose rather than golf for clarity
        if relx > 0:
            # Check if opposite key held down
            if "left" in self.pressed_keys:
                self.pressed_keys.remove("left")
                if not self.test_mode:
                    pag.keyUp("left")
            # Check that not already being held down
            if "right" not in self.pressed_keys:
                self.pressed_keys.append("right")
                # Hold the key down
                if not self.test_mode:
                    pag.keyDown("right")
                else:
                    print("Pressing right key")
        elif relx < 0:
            # Check if opposite key held down
            if "right" in self.pressed_keys:
                self.pressed_keys.remove("right")
                if not self.test_mode:
                    pag.keyUp("right")
            # Check that not already being held down
            if "left" not in self.pressed_keys:
                self.pressed_keys.append("left")
                # Hold the key down
                if not self.test_mode:
                    pag.keyDown("left")
                else:
                    print("Pressing left key")
        else:
            # Handling for case where = 0, need to remove both keys
            if "right" in self.pressed_keys:
                self.pressed_keys.remove("right")
                if not self.test_mode:
                    pag.keyUp("right")
            if "left" in self.pressed_keys:
                self.pressed_keys.remove("left")
                if not self.test_mode:
                    pag.keyUp("left")

        # Handling for y-dir next
        if rely > 0:
            # Check if opposite key held down
            if "down" in self.pressed_keys:
                self.pressed_keys.remove("down")
                if not self.test_mode:
                    pag.keyUp("down")
            # Check that not already being held down
            if "up" not in self.pressed_keys:
                self.pressed_keys.append("up")
                # Hold the key down
                if not self.test_mode:
                    pag.keyDown("up")
                else:
                    print("Pressing up key")
        elif rely < 0:
            # Check if opposite key held down
            if "up" in self.pressed_keys:
                self.pressed_keys.remove("up")
                if not self.test_mode:
                    pag.keyUp("up")
            # Check that not already being held down
            if "down" not in self.pressed_keys:
                self.pressed_keys.append("down")
                # Hold the key down
                if not self.test_mode:
                    pag.keyDown("down")
                else:
                    print("Pressing down key")
        else:
            # Handling for case where = 0, need to remove both keys
            if "up" in self.pressed_keys:
                self.pressed_keys.remove("up")
                if not self.test_mode:
                    pag.keyUp("up")
            if "down" in self.pressed_keys:
                self.pressed_keys.remove("down")
                if not self.test_mode:
                    pag.keyUp("down")

    def click(self, x, y):
        pass
