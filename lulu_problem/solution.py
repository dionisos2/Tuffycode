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

    def __repr__(self):
        result = ""
        for move in self.path:
            result += str(move)+"→"
        return result

def get_solution(board):
    current_paths = []
    for x in range(0, board.xmax//2):
        for y in range(0, board.ymax//2):
            path = Path(board)
            path.add_move((x, y))
            current_paths.append(path)

    # print(current_paths)
    for step in range(board.xmax*board.ymax-1):
        new_current_paths = []
        for path in current_paths:
            new_current_paths += get_next_paths(path)
        current_paths = new_current_paths
        # print(current_paths)

    return len(current_paths)*4



def get_next_paths(path):
    result = []

    for move in path.get_next_moves():
        new_path = deepcopy(path)
        new_path.add_move(move)
        result.append(new_path)
    return result

board = Board(4,6)
print(get_solution(board))
