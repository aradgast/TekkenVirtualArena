import cv2 as cv
from keyboard_infr import KeyBoardInterface as KI
import time
from grid import Grid

class Player:
    def __init__(self, player_num, dict):
        self.player_num = player_num
        self.dict = dict
        self.height = None
        self.width = None
        self.background = None
        self.center = None
        self.keyboard = KI()
        self.kick_flag = False
        self.punch_flag = False
        self.pressed_move_key = None

        # initialize the player source
        source = input(f"Enter the source of the video for player{player_num}: ")
        if source.isnumeric():
            self.source = int(source)
        else:
            self.source = source

        # initialize the player video capture
        self.cap = cv.VideoCapture(self.source)

        # initialize the player background
        self.__get_background()
        self.cap = cv.VideoCapture(self.source)

        # initialize the player height and width
        self.__get_height_and_width()
        self.cap = cv.VideoCapture(self.source)

        alpha = 1.5
        width = int(self.width * alpha)
        height = int(self.height)  # (se
        self.grid = Grid(height, width * 3)

    def move(self, cx, cy):
        thrash_height = 50
        offset_height = 20
        thrash_width = 100
        cy = cy - offset_height
        if self.center[0] > cx + thrash_width:
            self.keyboard.PressKey(self.dict['right'])
            # cv2.putText(frame, f"Move: {'left'}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            self.pressed_move_key = 'right'
            print(f'right is pressed')
        elif self.center[0] < cx - thrash_width:
            self.keyboard.PressKey(self.dict['left'])
            # cv2.putText(frame, f"Move: {'right'}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            self.pressed_move_key = 'left'
            print(f'left is pressed')
        elif self.center[1] > cy + thrash_height:
            self.keyboard.PressKey(self.dict['up'])
            # cv2.putText(frame, f"Move: {'up'}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            self.pressed_move_key = 'up'
            print(f'up is pressed')
        elif self.center[1] < cy - thrash_height:
            self.keyboard.PressKey(self.dict['down'])
            # cv2.putText(frame, f"Move: {'down'}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            self.pressed_move_key = 'down'
            print(f'down is pressed')
        else:
            try:
                self.keyboard.ReleaseKey(self.dict['right'])
                self.keyboard.ReleaseKey(self.dict['left'])
                self.keyboard.ReleaseKey(self.dict['up'])
                self.keyboard.ReleaseKey(self.dict['down'])
                self.keyboard.ReleaseKey(self.dict['kick_right'])
                self.keyboard.ReleaseKey(self.dict['kick_left'])
                self.keyboard.ReleaseKey(self.dict['punch_right'])
                self.keyboard.ReleaseKey(self.dict['punch_left'])
                self.pressed_move_key = None
            except Exception as e:
                print("the key is not pressed", e)




    def action(self, diff_frame, center):
        key = self.grid.active(diff_frame, center)
        if key is not None:
            self.keyboard.pressNrelease(self.dict[key])
        # count_kick = 0
        # count_punch = 0
        # for contour in diff_contours:
        #     (x, y, w, h) = cv.boundingRect(contour)
        #     center_x = int(x + w // 2)
        #     center_y = int(y + h // 2)
        #     if cv.contourArea(contour) < 250:
        #         continue
        #     if 0 <= center_x <= frame.shape[0] / 3 and 0 <= center_y <= frame.shape[1] / 3:
        #         count_kick += 1
        #     if 0 <= center_x <= frame.shape[0] / 3 and frame.shape[1] / 3 <= center_y <= 2 * frame.shape[1] / 3:
        #         count_punch += 1
        #     cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw differences
        #     cv.circle(frame, (center_x, center_y), 1, (0, 0, 255), 4)
        #
        # if count_kick == 0:
        #     self.kick_flag = False
        #
        # if count_punch == 0:
        #     self.punch_flag = False
        #
        # act = count_kick + count_punch
        #
        # if (count_kick >= count_punch) and (self.kick_flag == False):
        #     key = 'kick_left'
        #     self.keyboard.pressNrelease(self.dict['kick_left'])
        #     print(f'kick_left is pressed')
        #     self.kick_flag = True
        # elif (count_kick < count_punch) and (self.punch_flag == False):
        #     key = 'punch_right'
        #     self.keyboard.pressNrelease(self.dict['punch_right'])
        #     print(f'punch_right is pressed')
        #     self.punch_flag = True

        # return key, act

    def draw_activation_grid(self, frame, cx, cy):
        alpha = 1.5
        width = int(self.width * alpha)
        height = int(self.height)  # (self.height * alpha)
        left = cx - width // 2
        top = cy - height // 2
        cv.rectangle(frame, (left - width, top), (left + (2 * width), top + height), (0, 0, 255), 2)
        cv.line(frame, (left, top), (left, top + height), (0, 255, 0), 2)
        cv.line(frame, (left + width, top), (left + width, top + height), (0, 255, 0), 2)
        cv.line(frame, (left - width, top + height // 3), (left + (2 * width), top + height // 3), (0, 255, 0), 2)
        cv.line(frame, (left - width, top + (2 * height) // 3), (left + (2 * width), top + (2 * height) // 3),
                (0, 255, 0), 2)



    def __get_height_and_width(self):
        print(f"press SPCAE when ready to acquire height and width for player {self.player_num}")
        while True:
            ret, original_frame = self.cap.read()
            frame = cv.absdiff(original_frame, self.background)
            if type(self.source) != int:
                frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
                frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)

            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(gray, (21, 21), 0)
            ret, thresh = cv.threshold(blur, 50, 255, cv.THRESH_BINARY)
            contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            sort_contours = sorted(contours, key=cv.contourArea)
            try:
                x, y, w, h = cv.boundingRect(sort_contours[-1])
            except: continue
            cv.rectangle(original_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv.imshow("get height and width for player {}".format(self.player_num), original_frame)
            cv.imshow("thresh", thresh)
            k = cv.waitKey(1)
            # time.sleep(1)  # !!!!!!!!!!!!!
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                if (input("are you sure? (y/n) ") == 'n'):
                    print("try again")
                    k = cv.waitKey(1)
                    continue
                print("height: {}, width: {}".format(h, w))
                self.cap.release()
                cv.destroyAllWindows()
                self.height, self.width = h, w
                self.center = (x + w // 2, y + h // 2)
                break

    def __get_background(self):
        # Get background image from source

        print(f"press SPCAE when ready to acquire background for player {self.player_num}")
        while True:
            ret, frame = self.cap.read()
            if type(self.source) != int:
                # frame = cv.flip(frame,1)
                frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
                frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)

            if not ret:
                print("ERROR - failed to grab frame")
                break

            cv.imshow("get background from player {}".format(self.player_num), frame)

            k = cv.waitKey(1)
            # time.sleep(1)  # !!!!!!!!!!!!!
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                if (input("are you sure? (y/n) ") == 'n'):
                    print("try again")
                    k = cv.waitKey(1)
                    continue
                cv.imshow("background", frame)
                self.cap.release()
                cv.destroyAllWindows()
                self.background = frame
                break
