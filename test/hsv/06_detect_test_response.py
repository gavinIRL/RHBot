import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter, grab_object_preset

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

filter, custom_rect = grab_object_preset(
    object_name="other_player_map_loc")
# WindowCapture.list_window_names()
# initialize the WindowCapture class
wincap = WindowCapture(custom_rect=list(
    map(lambda x: int(x*1.5), custom_rect)))

# initialize the Vision class
vision_object = Vision('otherplayer.jpg')
# initialize the trackbar window
vision_object.init_control_gui()

# limestone HSV filter
# hsv_filter = HsvFilter(0, 0, 0, 255, 255, 255, 0, 0, 0, 0)
hsv_filter = filter

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    # pre-process the image
    output_image = vision_object.apply_hsv_filter(screenshot, hsv_filter)
    filter_image = output_image.copy()
    # do object detection, this time grab the points
    rectangles = vision_object.find(
        output_image, threshold=0.41, epsilon=0.5)
    # draw the detection results onto the original image
    points = vision_object.get_click_points(rectangles)
    output_image = vision_object.draw_crosshairs(screenshot, points)
    # display the processed image
    cv.imshow('Matches', output_image)
    # cv.imshow('Filtered', filter_image)
    if len(points) == 1:
        # print(points)
        print("Other player is located relatively x={} y={}".format(
            points[0][0]-131, 107-points[0][1]))
        sleep(1)
    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    # loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
