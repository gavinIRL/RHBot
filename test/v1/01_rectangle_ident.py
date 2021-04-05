import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

sample_img = cv.imread('capture2.jpg', cv.IMREAD_UNCHANGED)


def detect(target):
    result = cv.matchTemplate(sample_img, target, cv.TM_CCOEFF_NORMED)
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
    else:
        print("Object not found")


def get_locations(result, image, threshold=0.8):
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    # print(locations)

    if locations:
        print("Found object")
        width = image.shape[1]
        height = image.shape[0]
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for loc in locations:
            # Determine the box positions
            top_left = loc
            bottom_right = (top_left[0] + width, top_left[1] + height)
            # Draw the box
            cv.rectangle(sample_img, top_left, bottom_right,
                         line_color, line_type)

        cv.imshow('Matches', sample_img)
        cv.waitKey()
    else:
        print('Needle not found.')


if __name__ == "__main__":
    target = 'enemy.jpg'
    #target = "player_nodir.jpg"
    target_img = cv.imread(target, cv.IMREAD_UNCHANGED)
    get_locations(detect(target_img), target_img)
