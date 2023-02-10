import cv2
import numpy as np

# Read in a live video stream
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        exit()
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the frame to reduce noise
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Threshold the image to create a binary image
    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    sort_contours = sorted(contours, key=cv2.contourArea)
    c = sort_contours[-1]
    # c1 = sort_contours[-2]

    # Draw the contour on the frame
    cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
    # cv2.drawContours(frame, [c1], -1, (0, 100, 100), 2)

    # Find the center of mass of the contour
    M = cv2.moments(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    # Draw the center of mass on the frame
    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    # Find the bounding box of the contour
    x,y,w,h = cv2.boundingRect(c)

    # Draw the bounding box on the frame
    cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

    # Find the head, arms, and legs using the bounding box
    head_y = y + int(h/3)
    arms_y = y + int(h/3*2)
    legs_y = y + h
    left_x = x
    right_x = x + w
    center_x = x + int(w/2)

    # Draw the head, arms, and legs on the frame
    # cv2.line(frame, (left_x, head_y), (right_x, head_y), (0,255,0), 2)
    # cv2.line(frame, (left_x, arms_y), (right_x, arms_y), (0,255,0), 2)
    # cv2.line(frame, (left_x, legs_y), (right_x, legs_y), (0,255,0), 2)
    # cv2.line(frame, (center_x, y), (center_x, legs_y), (0,255,0), 2)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
# vid.release()
# Destroy all the windows
cv2.destroyAllWindows()



