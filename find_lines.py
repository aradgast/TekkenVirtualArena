import cv2 as cv
import numpy as np
from legend import *

def find_lines(frame, hight):
    print('ssearching for lines in frame')
    count = 0
    dst = cv.Canny(frame, CANNY_LOW, CANNY_HIGH, None, 3)
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    linesP = cv.HoughLinesP(dst, RHO, np.pi / THETA_RES, threshold=HOUGHLINE_THRESHOLD, minLineLength=MIN_LINE_LENGTH * hight, maxLineGap=MAX_LINE_GAP)
    eps = FIND_LINES_EPS

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            try:
                theta = np.arctan((l[3] - l[1]) / (l[2] - l[0]))
                # if np.pi / 4 - eps < theta < np.pi / 4 + eps or 3 * np.pi / 4 - eps < theta < 3 * np.pi / 4 + eps:
                #     count += 1
                #     print(f'found line pi/4 in frame')
                #     cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv.LINE_AA)
                # elif np.pi / 6 - eps < theta < np.pi / 6 + eps or 5 * np.pi / 6 - eps < theta < 5 * np.pi / 6 + eps:
                #     count += 1
                #     print(f'found line pi/6 in frame')
                #     cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0, 255, 0), 1, cv.LINE_AA)
                if np.pi / 2 + eps/2 < np.pi + theta < np.pi / 2 + 2 * eps or np.pi / 2 - 2 * eps < theta < np.pi / 2 - eps/2:
                    count += 1
                    # print(f'found line pi/2 in frame')
                    cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (255, 0, 0), 1, cv.LINE_AA)
                # elif np.pi / 3 - eps < theta < np.pi / 3 + eps or 2 * np.pi / 3 - eps < theta < 2 * np.pi / 3 + eps:
                #     count += 1
                #     print(f'found line pi/3 in frame')
                #     cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (100, 0, 100), 1, cv.LINE_AA)
                # elif - eps < theta < eps or np.pi - eps < theta < np.pi + eps:
                #     count += 1
                #     print(f'found line 0 in frame')
                #     cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0, 100, 100), 1, cv.LINE_AA)
                # elif 3 * np.pi /5 - eps < theta < 3 * np.pi /5 + eps:
                #     count += 1
                #     print(f'found line 3pi/5 in frame')
                #     cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (100, 100, 0), 1, cv.LINE_AA)
            except ZeroDivisionError:
                pass
    cv.imshow('find lines in frame', cdst)
    cv.waitKey(1)
    return count > 0

if __name__ == '__main__':
    cap = cv.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if ret:
            find_lines(frame)
        else:
            break