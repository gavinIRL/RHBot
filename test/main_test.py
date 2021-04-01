import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

sample_img = cv.imread('capture2.jpg', cv.IMREAD_UNCHANGED)


def detect(target):
    result = cv.matchTemplate(sample_img, target_img, cv.TM_CCOEFF_NORMED)

    return result


def show_result(result):
    cv.imshow("Result", result)
    cv.waitKey()


def get_min_max(result, image, threshold=0.8):
    _min_val, max_val, _min_loc, max_loc = cv.minMaxLoc(result)
    if max_val >= threshold:
        print("Found object, best match at x={}, y={}".format(
            max_loc[0], max_loc[1]))
        width = image.shape[1]
        height = image.shape[0]

        bottom_right = (max_loc[0] + width, max_loc[1] + height)
        cv.rectangle(sample_img, max_loc, bottom_right, color=(
            0, 255, 0), thickness=2, lineType=cv.LINE_4)

        cv.imshow("Rectangle", sample_img)
        cv.waitKey()


if __name__ == "__main__":
    #target = 'enemy.jpg'
    target = "player_nodir.jpg"
    target_img = cv.imread(target, cv.IMREAD_UNCHANGED)
    get_min_max(detect(target_img), target_img)
