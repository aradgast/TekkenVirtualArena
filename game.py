import time

import cv2 as cv
from keyboard_infr import KeyBoardInterface as KI
import matplotlib.pyplot as plt


class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        # self.center = center
        self.squares = []
        self.centers = []

        self.__create_squares()

    def __create_squares(self):
        # create the squares
        for i in range(3):
            for j in range(3):
                self.squares.append(Square(self.height // 3, self.width // 3))

    def _get_squares_centers(self, center):
        # get the squares centers
        for i in range(3):
            for j in range(3):
                self.centers.append((center[0] - self.width // 2 + self.width // 6 + self.width // 3 * j,
                                     center[1] - self.height // 2 + self.height // 6 + self.height // 3 * i))

    def active(self, diff_frame, center):
        self.centers = []
        self._get_squares_centers(center)
        for i in range(9):
            self.squares[i].active(diff_frame, self.centers[i])

        if self.squares[3].active_flag and self.squares[6].active_flag:
            print('kick_right')
            return 'kick_right'
        elif self.squares[0].active_flag:
            print('punch_left')
            return 'punch_left'


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


class Game:
    def __init__(self, num_players=1, source=None):
        self.symb_to_hex_player2 = {'up': 0x48,
                                    'left': 0x4B,
                                    'right': 0x4D,
                                    'down': 0x50,
                                    'punch_left': 0x31,  # 'n': 0x31 square
                                    'punch_right': 0x25,  # 'k': 0x25 triangle
                                    'kick_left': 0x32,  # 'm': 0x32 x
                                    'kick_right': 0x24}  # 'j': 0x24 circle

        self.symb_to_hex_player1 = {'up': 0xC8,
                                    'left': 0xCB,
                                    'right': 0xCD,
                                    'down': 0xD0,
                                    'punch_left': 0x1F,  # 's': 0x1F square
                                    'punch_right': 0x20,  # 'd': 0x20 triangle
                                    'kick_left': 0x2C,  # 'z': 0x2C x
                                    'kick_right': 0x2D}  # 'x': 0x2D circle

        self.symb_to_hex = [self.symb_to_hex_player1, self.symb_to_hex_player2]

        self.num_players = num_players
        self.players = [Player(i, self.symb_to_hex[i - 1]) for i in range(1, num_players + 1)]
        print("initialized game with {} players".format(num_players))

    def play(self):

        while True:
            for player in self.players:
                ret, original_frame = player.cap.read()
                frame = cv.absdiff(original_frame, player.background)
                time.sleep(0.001)
                ret, frame2 = player.cap.read()
                frame2 = cv.absdiff(frame2, player.background)
                if type(player.source) != int:
                    original_frame = cv.rotate(original_frame, cv.ROTATE_90_CLOCKWISE)
                    original_frame = cv.rotate(original_frame, cv.ROTATE_90_CLOCKWISE)
                    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
                    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
                    frame2 = cv.rotate(frame2, cv.ROTATE_90_CLOCKWISE)
                    frame2 = cv.rotate(frame2, cv.ROTATE_90_CLOCKWISE)
                if not ret:
                    exit()

                diff = cv.absdiff(frame, frame2)

                # Convert the frame to grayscale
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                # diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)

                # Blur the frame to reduce noise
                blur = cv.GaussianBlur(gray, (21, 21), 0)
                # diff_blur = cv.GaussianBlur(diff_gray, (5, 5), 0)

                # Threshold the image to create a binary image
                ret, thresh = cv.threshold(blur, 50, 255, cv.THRESH_BINARY)
                # ret, diff_thresh = cv.threshold(diff_blur, 50, 255, cv.THRESH_BINARY)

                thresh = cv.dilate(thresh, None, iterations=3)

                # Find contours in the binary image
                contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                # diff_contours, diff_hierarchy = cv.findContours(diff_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                # key, act, kick_flag, punch_flag = self.action(diff_contours, frame, kick_flag, punch_flag)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!

                # if act and not punch_flag and not kick_flag:
                #     kick_flag = True
                #     keyboard.pressNrelease(dict[key])
                #     print(f'{key} is pressed')
                #     # cv2.putText(frame, f"Status: {key}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                # Find the largest contour
                sort_contours = sorted(contours, key=cv.contourArea)
                try:
                    c = sort_contours[-1]
                    # c1 = sort_contours[-1]
                    # Draw the contour on the frame
                    # cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                    # cv2.drawContours(frame, [c1], -1, (0, 100, 100), 2)

                    # Find the center of mass of the contour
                    M = cv.moments(c)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    # Draw the center of mass on the frame
                    cv.circle(original_frame, (cx, cy), 5, (0, 0, 255), -1)

                    # check if the player moved
                    player.move(cx, cy)
                    player.action(diff, (cx, cy))

                    # Find the bounding box of the contour
                    x, y, w, h = cv.boundingRect(c)
                    player.draw_activation_grid(original_frame, cx, cy)

                    # Draw the bounding box on the frame
                    cv.rectangle(original_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # Find the head, arms, and legs using the bounding box
                    head_y = y + int(h / 3)
                    arms_y = y + int(h / 3 * 2)
                    legs_y = y + h
                    left_x = x
                    right_x = x + w
                    center_x = x + int(w / 2)
                    # Draw the head, arms, and legs on the frame
                    # cv2.line(frame, (left_x, head_y), (right_x, head_y), (0,255,0), 2)
                    # cv2.line(frame, (left_x, arms_y), (right_x, arms_y), (0,255,0), 2)
                    # cv2.line(frame, (left_x, legs_y), (right_x, legs_y), (0,255,0), 2)
                    # cv2.line(frame, (center_x, y), (center_x, legs_y), (0,255,0), 2)

                    # Display the resulting frame
                    cv.imshow(f"player{player.player_num}", original_frame)
                    cv.imshow("thresh", thresh)
                    # cv2.imshow('ret', diff_thresh)
                    cv.waitKey(1)

                    # Break the loop if the user presses 'q'
                except Exception as e:
                    print(e)
                    pass

                # return kick_flag, center


if __name__ == '__main__':
    g = Game(1)
    g.play()
