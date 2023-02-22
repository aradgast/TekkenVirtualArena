import cv2 as cv
import numpy as np
from legend import *

def find_lines(frame):
    print('ssearching for lines in frame')
    count = 0
    dst = cv.Canny(frame, CANNY_LOW, CANNY_HIGH, None, 3)
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    linesP = cv.HoughLinesP(dst, 4, np.pi / 180, threshold=35, minLineLength=10, maxLineGap=50)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            try:
                theta = np.arctan((l[3] - l[1]) / (l[2] - l[0]))
                if np.pi / 4 - 0.1 < theta < np.pi / 4 + 0.1: #or 3 * np.pi / 4 - 0.1 < theta < 3 * np.pi / 4 + 0.1 or np.pi / 6 - 0.1 < theta < np.pi / 6 + 0.1:
                    count += 1
                    print(f'found line pi/4 in frame')
                    cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv.LINE_AA)
                elif np.pi / 6 - 0.1 < theta < np.pi / 6 + 0.1: #or 3 * np.pi / 4 - 0.1 < theta < 3 * np.pi / 4 + 0.1 or np.pi / 6 - 0.1 < theta < np.pi / 6 + 0.1:
                    count += 1
                    print(f'found line pi/6 in frame')
                    cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0, 255, 0), 1, cv.LINE_AA)
                elif np.pi / 2 - 0.1 < theta < np.pi / 2 + 0.1: #or 3 * np.pi / 4 - 0.1 < theta < 3 * np.pi / 4 + 0.1 or np.pi / 6 - 0.1 < theta < np.pi / 6 + 0.1:
                    count += 1
                    print(f'found line pi/2 in frame')
                    cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (255, 0, 0), 1, cv.LINE_AA)
                elif np.pi / 3 - 0.1 < theta < np.pi / 3 + 0.1: #or 3 * np.pi / 4 - 0.1 < theta < 3 * np.pi / 4 + 0.1 or np.pi / 6 - 0.1 < theta < np.pi / 6 + 0.1:
                    count += 1
                    print(f'found line pi/3 in frame')
                    cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (100, 100, 100), 1, cv.LINE_AA)
            except ZeroDivisionError:
                pass
    cv.imshow('find lines in frame', cdst)
    cv.waitKey(1)
    return count > 0

if __name__ == '__main__':
    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            find_lines(frame)
        else:
            break