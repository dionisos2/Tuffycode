from board import *
from copy import deepcopy

class Path:
    DMOVES = [[-3,0], [3,0], [0,3], [0,-3], [2,2], [2,-2], [-2,2], [-2,-2]]

    def __init__(self, board):
        self.xmax = board.xmax
        self.ymax = board.ymax
        self.path = []
    def add_move(self, move):
        self.path.append(move)

    @property
    def current_pos(self):
        return self.path[-1]

    def move_possible(self, move):
        x, y = move
        return (0 <= x < self.xmax) and (0 <= y < self.ymax) and move not in self.path

    def get_next_moves(self):
        result = []
        x, y = self.current_pos
        for dmove in Path.DMOVES:
            move = (dmove[0]+x, dmove[1]+y)

            if self.move_possible(move):
                result.append(move)

        return result

def get_solution(board):
    current_path = []
    for x in range(0, board.xmax//2):
        for y in range(0, board.ymax//2):
            path = Path(board)
            path.add_move((x, y))
            current_path.append(path)

    for step in range(board.xmax*board.ymax):
        new_current_path = []
        for path in current_path:
            new_current_path += get_next_paths(path)
        current_path = new_current_path

    return len(current_path)



def get_next_paths(path):
    result = []

    for move in path.get_next_moves():
        new_path = deepcopy(path)
        new_path.add_move(move)
        result.append(new_path)
    return result

board = Board(4,5)
print(get_solution(board))
