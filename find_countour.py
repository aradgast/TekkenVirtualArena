import cv2
import numpy as np
import time

from keyboard_infr import KeyBoardInterface as KI

symb_to_hex_player1 = {'up': 0x48,
                       'left': 0x4B,
                       'right': 0x4D,
                       'down': 0x50,
                       'punch_left': 0x31,  # 'n': 0x31 square
                       'punch_right': 0x25,  # 'k': 0x25 triangle
                       'kick_left': 0x32,  # 'm': 0x32 x
                       'kick_right': 0x24}  # 'j': 0x24 circle

symb_to_hex_player2 = {'up': 0xC8,
                       'left': 0xCB,
                       'right': 0xCD,
                       'down': 0xD0,
                       'punch_left': 0x1F,  # 's': 0x1F square
                       'punch_right': 0x20,  # 'd': 0x20 triangle
                       'kick_left': 0x2C,  # 'z': 0x2C x
                       'kick_right': 0x2D}  # 'x': 0x2D circle


def action(diff_contours, frame, kick_flag, punch_flag):
    count_kick = 0
    count_punch = 0
    for contour in diff_contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        center_x = int(x + w // 2)
        center_y = int(y + h // 2)
        if cv2.contourArea(contour) < 250:
            continue
        if 0 <= center_x <= frame.shape[0] / 3 and 0 <= center_y <= frame.shape[1] / 3:
            count_kick += 1
        if 0 <= center_x <= frame.shape[0] / 3 and frame.shape[1] / 3 <= center_y <= 2 * frame.shape[1] / 3:
            count_punch += 1
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # draw differences
        cv2.circle(frame, (center_x, center_y), 1, (0, 0, 255), 4)

    if count_kick == 0:
        kick_flag = False

    if count_punch == 0:
        punch_flag = False

    act = count_kick + count_punch

    if count_kick >= count_punch:
        key = 'kick_left'
    else:
        key = 'punch_right'

    return key, act, kick_flag, punch_flag


def play(cap, kick_flag, punch_flag, name, dict, keyboard, center):
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
        keyboard.pressNrelease(dict[key])
        print(f'{key} is pressed')
        # cv2.putText(frame, f"Status: {key}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    # Find the largest contour
    sort_contours = sorted(contours, key=cv2.contourArea)
    try:
        c = sort_contours[-2]

        # Draw the contour on the frame
        # cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
        # cv2.drawContours(frame, [c1], -1, (0, 100, 100), 2)

        # Find the center of mass of the contour
        M = cv2.moments(c)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # Draw the center of mass on the frame
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        if center is None:
            center = (cx, cy)
        else:
            if center[0] > cx+50:
                keyboard.pressNrelease(dict['left'])
                center = (cx, cy)
                # cv2.putText(frame, f"Move: {'left'}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                print(f'left is pressed')
            elif center[0] < cx-50:
                keyboard.pressNrelease(dict['right'])
                center = (cx, cy)
                # cv2.putText(frame, f"Move: {'right'}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                print(f'right is pressed')
            elif center[1] > cy+50:
                keyboard.pressNrelease(dict['up'])
                center = (cx, cy)
                # cv2.putText(frame, f"Move: {'up'}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                print(f'up is pressed')
            elif center[1] < cy-50:
                keyboard.pressNrelease(dict['down'])
                center = (cx, cy)
                # cv2.putText(frame, f"Move: {'down'}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                print(f'down is pressed')

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
    return kick_flag, center


if __name__ == '__main__':
    # Read in a live video stream
    cap1 = cv2.VideoCapture(r"C:\Users\aradg\OneDrive - post.bgu.ac.il\data\ComputerVision\video_arad\arad3.mp4")
    # cap2 = cv2.VideoCapture(r"C:\Users\aradg\OneDrive - post.bgu.ac.il\data\ComputerVision\video_arad\itamar2.mp4")
    keyboard1 = KI()
    keyboard2 = KI()

    kick_flag1 = False
    kick_flag2 = False
    punch_flag1 = False
    punch_flag2 = False

    center1 = None
    center2 = None

    while True:
        # Capture frame-by-frame
        time.sleep(0.05)
        kick_flag1, center1 = play(cap1, kick_flag1, punch_flag1, 'cap1', symb_to_hex_player1, keyboard1, center1)
        # kick_flag2, center2 = play(cap2, kick_flag2, punch_flag2, 'cap2', symb_to_hex_player2, keyboard2, center2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # After the loop release the cap object
    # vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
