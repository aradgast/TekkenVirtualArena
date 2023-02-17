import cv2 as cv
class Game:
    def __init__(self, num_players = 1, source = None):
        self.num_players = num_players
        self.sources = [source] if source else [None] * num_players
        for i in range(num_players):
             source = input("Enter source for player {}: ".format(i + 1))
             if source.isnumeric():
                 self.sources[i] = int(source)
             else:
                 self.sources[i] = source

        print('Game initialized with {} players'.format(self.num_players))
        print('Take an image of the background from each source')
        self.backgrounds = [None] * num_players
        for i in range(num_players):
            self.backgrounds[i] = self.get_background(i)
            print('Background for player {} acquired'.format(i + 1))

        for background in self.backgrounds:
            cv.imshow('background', background)
            cv.waitKey(0)
            cv.destroyAllWindows()



    def get_background(self, player):
        # Get background image from source
        cam = cv.VideoCapture(self.sources[player])

        cv.namedWindow("get background from source {}".format(player + 1))

        img_counter = 0
        print(f"press SPCAE when ready")
        while True:
            ret, frame = cam.read()
            if type(self.sources[player]) != int:
                frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
                frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
            if not ret:
                print("failed to grab frame")
                break

            cv.imshow("get background from source {}".format(player + 1), frame)


            k = cv.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                cam.release()
                cv.destroyAllWindows()
                return frame

if __name__ == '__main__':
    g = Game(1)

