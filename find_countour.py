import cv2 as cv
from game import Game
from keyboard_infr import KeyBoardInterface as KI
import time

if __name__ == '__main__':
    game = Game()
    # Read in a live video stream
    # cap1 = cv.VideoCapture(r"C:\Users\aradg\OneDrive - post.bgu.ac.il\data\ComputerVision\video_arad\arad3.mp4")
    # cap2 = cv2.VideoCapture(r"C:\Users\aradg\OneDrive - post.bgu.ac.il\data\ComputerVision\video_arad\itamar2.mp4")
    keyboard1 = KI()
    keyboard2 = KI()

    kick_flag1 = False
    kick_flag2 = False
    punch_flag1 = False
    punch_flag2 = False

    center1 = None
    center2 = None
    flag = True
    while True:
        # Capture frame-by-frame
        time.sleep(0.05)
        kick_flag1, center1 = game.play(cap1, kick_flag1, punch_flag1, 'cap1', game.symb_to_hex_player1, keyboard1, center1, flag)
        flag = False
        # kick_flag2, center2 = play(cap2, kick_flag2, punch_flag2, 'cap2', symb_to_hex_player2, keyboard2, center2)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    # After the loop release the cap object
    # vid.release()
    # Destroy all the windows
    cv.destroyAllWindows()