import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def detect_enemy():
    target_img = cv.imread(
        'enemy.jpg', cv.IMREAD_UNCHANGED)
    sample_img = cv.imread(
        'capture2.jpg', cv.IMREAD_UNCHANGED)

    result = cv.matchTemplate(sample_img, target_img, cv.TM_CCOEFF_NORMED)

    cv.imshow("Result", result)
    cv.waitKey()


def detect_player():
    target_img = cv.imread(
        'player_down.jpg', cv.IMREAD_UNCHANGED)
    sample_img = cv.imread(
        'capture2.jpg', cv.IMREAD_UNCHANGED)

    result = cv.matchTemplate(sample_img, target_img, cv.TM_CCOEFF_NORMED)

    cv.imshow("Result", result)
    cv.waitKey()


if __name__ == "__main__":
    detect_player()
