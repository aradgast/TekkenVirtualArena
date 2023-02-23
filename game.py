import time
import cv2 as cv
from player import Player
from legend import *
from keyboard_infr import KeyBoardInterface as KI
import numpy as np

class Game:
    def __init__(self, num_players=1, caps = None, sources = None):
        self.symb_to_hex_player2 = {'up': 0x09,
                                    'left': 0x05,
                                    'right': 0x07,
                                    'down': 0x03,
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
        self.keyboard = KI()
        self.num_players = num_players

        if caps is None:
            self.players = [Player(i, self.symb_to_hex[i - 1], self.keyboard) for i in range(1, num_players + 1)]
            self.caps = [player.cap for player in self.players]
            self.sources = [player.source for player in self.players]
        else:
            self.players = [Player(i, self.symb_to_hex[i - 1], self.keyboard, self.caps[i-1], self.sources[i-1]) for i in range(1, num_players + 1)]
        print("initialized game with {} players".format(num_players))

    def play(self):
        for i in range(5):
            print("starting in {} seconds".format(5-i))
            time.sleep(1)
        print("starting now!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        while True:
            for player in self.players:
                ret, original_frame = player.cap.read()
                if type(player.source) != int:
                    original_frame = cv.rotate(original_frame, cv.ROTATE_90_CLOCKWISE)
                    original_frame = cv.rotate(original_frame, cv.ROTATE_90_CLOCKWISE)
                frame = cv.absdiff(original_frame, player.background)  # subtract background
                time.sleep(0.001)
                ret, frame2 = player.cap.read()
                if type(player.source) != int:
                    frame2 = cv.rotate(frame2, cv.ROTATE_90_CLOCKWISE)
                    frame2 = cv.rotate(frame2, cv.ROTATE_90_CLOCKWISE)
                frame2 = cv.absdiff(frame2, player.background)  # subtract background
                if not ret:
                    exit()

                diff = cv.absdiff(frame, frame2)
                if np.sum(diff) < GAME_DIFF_THRESHOLD:
                    continue
                # Convert the frame to grayscale
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)

                # Blur the frame to reduce noise
                blur = cv.GaussianBlur(gray, GAUSS_KERNEL, 0)
                diff_blur = cv.GaussianBlur(diff_gray, GAUSS_KERNEL, 0)

                for i in range(MEDIAN_FILTER):
                    blur = cv.medianBlur(blur, MEDIAN_KERNEL)
                    diff_blur = cv.medianBlur(diff_blur, MEDIAN_KERNEL)

                # Threshold the image to create a binary image
                ret, thresh = cv.threshold(blur, player.binary_thresh, 255, cv.THRESH_BINARY)
                ret, diff_thresh = cv.threshold(diff_blur, player.binary_thresh, 255, cv.THRESH_BINARY)

                thresh = cv.dilate(thresh, None, iterations=3)
                diff_thresh = cv.dilate(diff_thresh, None, iterations=3)

                # Find contours in the binary image
                contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

                # Find the largest contour
                sort_contours = sorted(contours, key=cv.contourArea, reverse=True)
                try:

                    for contour in sort_contours:
                        if cv.contourArea(contour) >= frame.shape[0] * frame.shape[1] * FRAME_AREA_THRESHOLD:
                            continue
                        else:
                            c = contour
                            break
                    # Find the center of mass of the contour
                    M = cv.moments(c)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    # Draw the center of mass on the frame
                    cv.circle(original_frame, (cx, cy), 5, (0, 0, 255), -1)

                    # check if the player moved
                    player.move(cx, cy)
                    player.action(diff_thresh, (cx, cy), gray)

                    # Find the bounding box of the contour
                    x, y, w, h = cv.boundingRect(c)
                    player.draw_activation_grid(original_frame, cx, cy)

                    # Draw the bounding box on the frame
                    cv.rectangle(original_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # Display the resulting frame
                    cv.imshow(f"player{player.player_num}", original_frame)
                    cv.imshow("thresh", thresh)
                    cv.imshow('diff_thresh', diff_thresh)
                    cv.waitKey(1)

                except Exception as e:
                    print(e)
                    pass
            # write a condition to wait to an Esc key press to exit the game
            if cv.waitKey(1) == 27:
                print('NEW GAME')
                self.__init__(self.num_players, self.caps, self.sources)
                for i in range(5):
                    print("starting in {} seconds".format(5 - i))
                    time.sleep(1)
                print("starting now!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                continue

if __name__ == '__main__':
    g = Game(1)
    g.play()
