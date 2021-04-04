# This is to figure out what does and doesn't work in the game
# Having issues where nothing is being sent to the game
import pyautogui
import pydirectinput
import time


def test_move():
    time.sleep(4)
    pydirectinput.keyDown('left')
    time.sleep(1)
    pydirectinput.keyUp('left')


def loop_move():
    time.sleep(3)
    count = 0
    pydirectinput.keyDown("left")
    while count < 5:
        time.sleep(0.1)
        count += 1
    else:
        pydirectinput.keyUp("left")


loop_move()
