import cv2 as cv


class Square:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.active_flag = False
        self.count = 0
        self.init_count = 3
        self.active_threshold = 50

    def active(self, diff_thresh, center):
        x_min = max(0, center[0] - self.width // 2)
        x_max = min(diff_thresh.shape[1], center[0] + self.width // 2)
        y_min = max(0, center[1] - self.height // 2)
        y_max = min(diff_thresh.shape[0], center[1] + self.height // 2)
        diff_thresh = diff_thresh[y_min: y_max, x_min:x_max]
        # cv.imshow('diff_frame', diff_frame)
        # cv.waitKey(1)
        # time.sleep(3)
        if self.active_flag:
            self.count -= 1
            if self.count <= 0:
                self.active_flag = False
        else:
            # diff_contours, diff_hierarchy = cv.findContours(diff_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            # for contour in diff_contours:
            #     if cv.contourArea(contour) > active_threshold:
            #         self.active_flag = True
            #         self.count = count
            #         break
            if cv.countNonZero(diff_thresh) > self.active_threshold:
                self.active_flag = True
                self.count = self.init_count


# write a class "middle square" that inherits from square, but get as activation threshold diffrent value, let's say 100

class MiddleSquare(Square):
    def __init__(self, height, width):
        super().__init__(height, width)
        self.active_threshold = 75
        self.init_count = 0