from board import *
from copy import deepcopy

class Path:
    DMOVES = [[-3,0], [3,0], [0,3], [0,-3], [2,2], [2,-2], [-2,2], [-2,-2]]

    def __init__(self, board):
        self.xmax = board.xmax
        self.ymax = board.ymax
        self.path = []
        #number of paths this path represent
        self.weight = 1

    def add_move(self, move):
        self.path.append(move)

    @property
    def current_pos(self):
        return self.path[-1]

    def move_possible(self, move, collision):
        x, y = move
        return (0 <= x < self.xmax) and (0 <= y < self.ymax) and ((not collision) or (move not in self.path))

    def get_next_moves(self, move=None, collision=True):
        result = []
        if move == None:
            x, y = self.current_pos
        else:
            x, y = move

        for dmove in Path.DMOVES:
            move = (dmove[0]+x, dmove[1]+y)

            if self.move_possible(move, collision):
                result.append(move)

        return result

    def __repr__(self):
        result = ""
        for move in self.path:
            result += str(move)+"→"
        return result

    def is_valid(self):
        #liberties[move]=number of liberty
        liberties = dict()

        for move in self.path[:-1]:
            for next_move in self.get_next_moves(move):
                if next_move in self.path:
                    continue
                if next_move in liberties:
                    liberties[next_move] -= 1
                    if liberties[next_move] == 0:
                        return False
                else:
                    liberties[next_move] = len(self.get_next_moves(next_move, False))-1
        return True

def remove_bad_paths(paths):
    print("-"*10)
    print(len(paths))
    new_paths = [path for path in paths if path.is_valid()]
    print(len(new_paths))
    return new_paths

def merge_paths(paths):
    return paths

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

        current_paths = remove_bad_paths(new_current_paths)
        current_paths = merge_paths(current_paths)
        # print(current_paths)

    return len(current_paths)*4



def get_next_paths(path):
    result = []

    for move in path.get_next_moves():
        new_path = deepcopy(path)
        new_path.add_move(move)
        result.append(new_path)
    return result

board = Board(6,  6)
print(get_solution(board))
