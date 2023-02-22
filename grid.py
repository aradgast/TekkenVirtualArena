import cv2 as cv
from find_lines import find_lines

from square import Square, MiddleSquare
import numpy as np
class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        # self.center = center
        self.squares = []
        self.centers = []
        self.prev_center = None
        self.center_vel = 0

        self.__create_squares()

    def __create_squares(self):
        # create the squares
        for i in range(3):
            for j in range(3):
                if j ==1 and (i == 1 or i == 0):
                    self.squares.append(MiddleSquare(self.height // 3, self.width // 3))
                else:
                    self.squares.append(Square(self.height // 3, self.width // 3))

    def _get_squares_centers(self, center):
        # get the squares centers
        for i in range(3):
            for j in range(3):
                self.centers.append((center[0] - self.width // 2 + self.width // 6 + self.width // 3 * j,
                                     center[1] - self.height // 2 + self.height // 6 + self.height // 3 * i))

    def active(self, diff_thresh, center, gray):
        if self.prev_center is None:
            self.prev_center = center
        else:
            self.center_vel = np.square(np.array(center[0]) - np.array(self.prev_center[0])).mean()
            self.prev_center = center
        self.centers = []
        self._get_squares_centers(center)
        for i in range(9):
            self.squares[i].active(diff_thresh, self.centers[i])

        if self.squares[3].active_flag and self.squares[6].active_flag:
            if self.center_vel > 10:
                print(f'center_vel: {self.center_vel}')
                return 'kick_right'
            else:
                print(f'center_vel: {self.center_vel}')
                return 'kick_left'
        elif self.squares[0].active_flag:
            try:
                x_min = max(0, self.centers[1][0] - self.width // 6)
                x_max = min(diff_thresh.shape[1], self.centers[1][0] + self.width // 6)
                y_min = max(0, self.centers[1][1] - self.height // 6)
                y_max = min(diff_thresh.shape[0], self.centers[1][1] + self.height // 6)
                gray = gray[y_min: y_max, x_min:x_max]
                is_right = find_lines(gray)
                if is_right:             # and self.squares[4].active_flag:
                    return 'punch_right'
                else:
                    return 'punch_left'
            except IndexError:
                print('IndexError')
                pass
            x_min = max(0, self.centers[1][0] - self.width // 2)
            x_max = min(diff_thresh.shape[1], self.centers[1][0] + self.width // 2)
            y_min = max(0, self.centers[1][1] - self.height // 2)
            y_max = min(diff_thresh.shape[0], self.centers[1][1] + self.height // 2)
            gray = gray[y_min: y_max, x_min:x_max]
            is_right = find_lines(gray)
            if is_right:             # and self.squares[4].active_flag:
                return 'punch_right'
            else:
                return 'punch_left'

        elif self.squares[5].active_flag and self.squares[8].active_flag:
            if self.center_vel > 10:
                return 'kick_right'
            else:
                print(f'center_vel: {self.center_vel}')
                return 'kick_left'
        elif self.squares[2].active_flag:
            if self.squares[4].active_flag:
                return 'punch_right'
            else:
                return 'punch_left'