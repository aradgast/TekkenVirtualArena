import time
import cv2 as cv
from player import Player


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
                                    'right': 0xCB,  # swiched left and right
                                    'left': 0xCD,
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
