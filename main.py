from game import Game
import cv2 as cv
import numpy as np
if __name__ == '__main__':
    g = Game(int(input("How many players to initiate? (1/2)")))
    g.play()
