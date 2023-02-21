from square import Square
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
            return 'kick_right'
        elif self.squares[0].active_flag:
            return 'punch_left'
        elif self.squares[5].active_flag and self.squares[8].active_flag:
            return 'kick_right'
        elif self.squares[2].active_flag:
            return 'punch_left'