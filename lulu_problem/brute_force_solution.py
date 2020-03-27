from board import *
from copy import deepcopy

DMOVES = [[-3,0], [3,0], [0,3], [0,-3], [2,2], [2,-2], [-2,2], [-2,-2]]
def possible_moves(board, current_pos):
    result = []
    x, y = current_pos
    for dmove in DMOVES:
        new_x = dmove[0]+x
        new_y = dmove[1]+y
        if ((0 <= new_x < board.xmax) and
            (0 <= new_y < board.ymax) and
            (board.matrix[new_x][new_y] == 0)):
            result.append((new_x, new_y))
    return result



def get_solution(board, current_pos=None, step=1):
    result = 0

    if step == (board.xmax*board.ymax)+1:
        print(board)
        return 1

    if current_pos == None:
        for x in range(board.xmax):
            for y in range(board.ymax):
                new_board = deepcopy(board)
                new_board.matrix[x][y] = step
                result += get_solution(new_board, (x, y), step+1)

    else:
        for move in possible_moves(board, current_pos):
            x, y = move
            new_board = deepcopy(board)
            new_board.matrix[x][y] = step
            result += get_solution(new_board, move, step+1)

    return result


board = Board(4,6)
print(get_solution(board))


