class Board:
    def __init__(self, xmax, ymax):
        self.matrix = [[0]*ymax for _ in range(xmax)]
        self.xmax = xmax
        self.ymax = ymax

    def __repr__(self):
        result = ""

        for y in range(self.ymax):
            for x in range(self.xmax):
                result += f"|{self.matrix[x][y]:03d}|"
            result += "\n"

        return result

