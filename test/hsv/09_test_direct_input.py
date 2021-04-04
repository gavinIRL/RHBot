# This is to figure out what does and doesn't work in the game
# Having issues where nothing is being sent to the game
import pyautogui
import pydirectinput
import time

time.sleep(4)
pydirectinput.keyDown('w')
time.sleep(1)
pydirectinput.keyUp('w')
