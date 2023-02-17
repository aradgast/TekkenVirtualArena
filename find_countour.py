import cv2
import numpy as np
import time

import keyboard_infr

symb_to_hex_player1 = {'w': 0x11, 'a': 0x1E, 's': 0x1F, 'd': 0x20, 'up': 0xC8, 'left': 0xCB, 'right': 0xCD,
                       'down': 0xD0,
                       'enter': 0x1C, 'esc': 0x01, 'two': 0x03, 'z': 0x2C, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F, 'b': 0x30,
                       'punch_left': 0x31, 'kick_left': 0x32, 'q': 0x10, 'e': 0x12, 'r': 0x13, 't': 0x14, 'y': 0x15,
                       'u': 0x16, 'i': 0x17,
                       'o': 0x18, 'p': 0x19, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'kick_right': 0x24, 'punch_right': 0x25,
                       'l': 0x26,
                       'space': 0x39, 'shift': 0x2A, 'ctrl': 0x1D, 'alt': 0x38, 'tab': 0x0F}

symb_to_hex_player2 = {'w': 0x11, 'a': 0x1E, 'punch_left': 0x1F, 'punch_right': 0x20, 'up': 0xC8, 'left': 0xCB,
                         'right': 0xCD, 'down': 0xD0,
                         'enter': 0x1C, 'esc': 0x01, 'two': 0x03, 'kick_left': 0x2C, 'x': 0x2D, 'c': 0x2E, 'v': 0x2F,
                         'b': 0x30,
                         'n': 0x31, 'm': 0x32, 'q': 0x10, 'e': 0x12, 'r': 0x13, 't': 0x14, 'y': 0x15, 'u': 0x16,
                         'i': 0x17,
                         'o': 0x18, 'p': 0x19, 'f': 0x21, 'g': 0x22, 'h': 0x23, 'j': 0x24, 'k': 0x25, 'l': 0x26,
                         'space': 0x39, 'shift': 0x2A, 'ctrl': 0x1D, 'alt': 0x38, 'tab': 0x0F}


def action(diff_contours, frame, kick_flag, punch_flag):
    count_kick = 0
    count_punch = 0
    for contour in diff_contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        center_x = int(x + w // 2)
        center_y = int(y + h // 2)
        if cv2.contourArea(contour) < 200:
            continue
        if 0 <= center_x <= frame.shape[0] / 3 and 0 <= center_y <= frame.shape[1] / 3:
            count_kick += 1
        if 0 <= center_x <= frame.shape[0] / 3 and frame.shape[1] / 3 <= center_y <= 2 * frame.shape[1] / 3:
            count_punch += 1
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),2)  # draw differences
        cv2.circle(frame, (center_x, center_y), 1, (0, 0, 255), 4)


    if count_kick == 0:
        kick_flag = False
        print('flag')

    if count_punch == 0:
        punch_flag = False
        print('flag')

    act = count_kick + count_punch

    if count_kick >= count_punch:
        key = 'kick_left'
    else:
        key = 'punch_right'

    return key, act, kick_flag, punch_flag


def play(cap, kick_flag, punch_flag, name, dict):
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    ret, frame2 = cap.read()
    frame2 = cv2.rotate(frame2, cv2.ROTATE_90_CLOCKWISE)
    frame2 = cv2.rotate(frame2, cv2.ROTATE_90_CLOCKWISE)
    if not ret:
        exit()

    diff = cv2.absdiff(frame, frame2)
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Blur the frame to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    diff_blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)

    # Threshold the image to create a binary image
    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
    ret, diff_thresh = cv2.threshold(diff_blur, 50, 255, cv2.THRESH_BINARY)

    dilated = cv2.dilate(thresh, None, iterations=3)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    diff_contours, diff_hierarchy = cv2.findContours(diff_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = 0
    key, act, kick_flag, punch_flag = action(diff_contours, frame, kick_flag, punch_flag)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!

    if act and not punch_flag and not kick_flag:
        kick_flag = True
        keyboard_infr.PressKey(dict[key])
        time.sleep(0.01)
        keyboard_infr.ReleaseKey(dict[key])
        cv2.putText(frame, f"Status: {key}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Find the largest contour
    sort_contours = sorted(contours, key=cv2.contourArea)
    try:
        c = sort_contours[-2]
        print(len(sort_contours))
        # c1 = sort_contours[-2]

        # Draw the contour on the frame
        # cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        # cv2.drawContours(frame, [c1], -1, (0, 100, 100), 2)

        # Find the center of mass of the contour
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # Draw the center of mass on the frame
        # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        # Find the bounding box of the contour
        x, y, w, h = cv2.boundingRect(c)

        # Draw the bounding box on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

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
        cv2.imshow(name, frame)
        # cv2.imshow('ret', diff_thresh)

        # Break the loop if the user presses 'q'
    except Exception as e:
        print(e)
        pass
    return kick_flag


if __name__ == '__main__':
    # Read in a live video stream
    cap1 = cv2.VideoCapture(r"C:\Users\aradg\OneDrive - post.bgu.ac.il\data\ComputerVision\video_arad\arad3.mp4")
    cap2 = cv2.VideoCapture(r"C:\Users\aradg\OneDrive - post.bgu.ac.il\data\ComputerVision\video_arad\itamar2.mp4")

    kick_flag1 = False
    kick_flag2 = False
    punch_flag1 = False
    punch_flag2 = False

    while True:
        # Capture frame-by-frame
        time.sleep(0.005)
        kick_flag1 = play(cap1, kick_flag1, punch_flag1, 'cap1', symb_to_hex_player1)
        kick_flag2 = play(cap2, kick_flag2, punch_flag2, 'cap2', symb_to_hex_player2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    # vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
