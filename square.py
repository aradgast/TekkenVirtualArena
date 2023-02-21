import cv2 as cv
class Square:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.active_flag = False
        self.count = 0

    def active(self, diff_frame, center):
        x_min = max(0, center[0] - self.width // 2)
        x_max = min(diff_frame.shape[1], center[0] + self.width // 2)
        y_min = max(0, center[1] - self.height // 2)
        y_max = min(diff_frame.shape[0], center[1] + self.height // 2)
        diff_frame = diff_frame[y_min: y_max, x_min:x_max]
        # cv.imshow('diff_frame', diff_frame)
        # cv.waitKey(1)
        # time.sleep(3)
        if self.active_flag:
            self.count -= 1
            if self.count == 0:
                self.active_flag = False
        else:
            diff_gray = cv.cvtColor(diff_frame, cv.COLOR_BGR2GRAY)
            diff_blur = cv.GaussianBlur(diff_gray, (11, 11), 0)
            diff_thresh = cv.threshold(diff_blur, 50, 255, cv.THRESH_BINARY)[1]
            diff_thresh = cv.dilate(diff_thresh, None, iterations=2)
            diff_contours, diff_hierarchy = cv.findContours(diff_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            for contour in diff_contours:
                if cv.contourArea(contour) > 250:
                    self.active_flag = True
                    self.count = 10
                    break
