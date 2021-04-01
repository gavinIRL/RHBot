import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def findObjectCentre(target_img_path, sample_img_path, threshold=0.8, graphic=None):
    sample_img = cv.imread(sample_img_path, cv.IMREAD_UNCHANGED)
    target_img = cv.imread(target_img_path, cv.IMREAD_UNCHANGED)
    width = target_img.shape[1]
    height = target_img.shape[0]
    result = cv.matchTemplate(sample_img, target_img, cv.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), width, height]
        # Prevent single results from being deleted
        rectangles.append(rect)
        rectangles.append(rect)
    rectangles, weights = cv.groupRectangles(
        rectangles, groupThreshold=1, eps=0.5)

    points = []
    if len(rectangles):
        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (x, y, w, h) in rectangles:
            middle_x = x + int(w/2)
            middle_y = y + int(h/2)
            points.append((middle_x, middle_y))

            if graphic == 'rectangles':
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                cv.rectangle(sample_img, top_left, bottom_right, color=line_color,
                             lineType=line_type, thickness=2)
            elif graphic == 'points':
                cv.drawMarker(sample_img, (middle_x, middle_y),
                              color=marker_color, markerType=marker_type,
                              markerSize=40, thickness=2)

        if graphic:
            cv.imshow('Matches', sample_img)
            cv.waitKey()

    return points


points = findObjectCentre(
    'enemy.jpg', 'capture2.jpg', threshold=0.8, graphic='points')
# print(points)
points = findObjectCentre('player_nodir.jpg', 'capture2.jpg',
                          threshold=0.70, graphic='points')
print(points)
print('Done.')
