import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter, grab_object_preset
from actions import Actions

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialise the actions object
actions = Actions(test_mode=True)

# The next block of code is for detecting the object in question
object_filter, object_custom_rect = grab_object_preset(
    object_name="other_player_map_loc")
# WindowCapture.list_window_names()
# This is only for testing and fixing the 150% screen scaling I have
# object_custom_rect = list(map(lambda x: int(x*1.5), object_custom_rect))
# initialize the WindowCapture class for object detection
object_wincap = WindowCapture(
    "Rusty Hearts: Revolution - Reborn ", custom_rect=object_custom_rect)
# initialize the Vision class
object_vision = Vision('otherplayer.jpg')
# initialize the trackbar window
# object_vision.init_control_gui()


# This block of code is for detecting if in a dungeon or not
dunchk_filter, dunchk_custom_rect = grab_object_preset(
    object_name="dungeon_check")
# This is only for testing and fixing the 150% screen scaling I have
# dunchk_custom_rect = list(map(lambda x: int(x*1.5), dunchk_custom_rect))
dunchk_wincap = WindowCapture(custom_rect=dunchk_custom_rect)
dunchk_vision = Vision('dunchk.jpg')


loop_time = time()
while(True):

    # get an updated image of the game at specified area
    dunchk_screenshot = dunchk_wincap.get_screenshot()
    # pre-process the image to help with detection
    dunchk_output_image = dunchk_vision.apply_hsv_filter(
        dunchk_screenshot, dunchk_filter)
    # do object detection, this time grab the points
    dunchk_rectangles = dunchk_vision.find(
        dunchk_output_image, threshold=0.27, epsilon=0.5)

    # then if currently in a dungeon search for object
    if len(dunchk_rectangles) == 1:
        # get an updated image of the game at map loc
        screenshot = object_wincap.get_screenshot()
        # then try to detect the other player
        output_image = object_vision.apply_hsv_filter(
            screenshot, object_filter)
        # filter_image = output_image.copy()
        # do object detection, this time grab the points
        rectangles = object_vision.find(
            output_image, threshold=0.41, epsilon=0.5)
        # draw the detection results onto the original image
        points = object_vision.get_click_points(rectangles)
        if len(points) == 1:
            output_image = object_vision.draw_crosshairs(screenshot, points)
            # If there is only one value found
            # i.e. no false positives and players are not on top of each other
            # Then figure out keypresses required to move towards other player
            # And then implement
            # print("Other player is located relatively x={} y={}".format(
            #     points[0][0]-131, 107-points[0][1]))
            actions.move_direction(points[0][0]-131, 107-points[0][1])
            sleep(0.1)
        else:
            # Clear all keypresses
            print("Can't detect other player, stopping movement")
            actions.stop_keypresses(movement_only=True)
            sleep(0.25)
        # display the processed image
        cv.imshow('Matches', output_image)
        # cv.imshow('Filtered', filter_image)
    else:
        print("Not in dungeon, slowing refresh rate")
        actions.stop_keypresses(movement_only=True)
        sleep(0.5)

    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    # loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
