from functools import lru_cache

DMOVES = [[-3,0], [3,0], [0,3], [0,-3], [2,2], [2,-2], [-2,2], [-2,-2]]
def possible_moves(xmax, ymax, current_pos):
    result = []
    x, y = current_pos
    for dmove in DMOVES:
        new_x = dmove[0]+x
        new_y = dmove[1]+y
        if (0 <= new_x < xmax) and (0 <= new_y < ymax):
            result.append((new_x, new_y))
    return result

def is_valid(xmax, ymax, squares, end_square):
    #Seems useless
    return True
    liberties = dict()

    for square in (squares-{end_square}):
        for next_move in possible_moves(xmax, ymax, square):
            if next_move in squares:
                continue
            if next_move in liberties:
                liberties[next_move] -= 1
                if liberties[next_move] == 0:
                    print("a")
                    return False
            else:
                liberties[next_move] = len(possible_moves(xmax, ymax, next_move))-1

    return True

def get_solution(xmax, ymax):


    squares = frozenset((x, y) for x in range(xmax) for y in range(ymax))
    start_squares = [(x, y) for x in range(xmax//2) for y in range(ymax//2)]

    paths_count = 0
    for square in start_squares:
        paths_count += get_paths_count(xmax, ymax, squares, square)

    paths_count *= 4

    middle_squares = []
    if xmax%2 == 1:
        middle_squares += [(xmax//2, y) for y in range(ymax)]
    if ymax%2 == 1:
        middle_squares += [(x, ymax//2) for x in range(xmax)]

    for square in middle_squares:
        paths_count += get_paths_count(xmax, ymax, squares, square)

    return paths_count


@lru_cache(maxsize=2**16)
def get_paths_count(xmax, ymax, squares, end_square):
    if len(squares) == 1:
        return 1

    if not is_valid(xmax, ymax, squares, end_square):
        return 0

    current_squares = squares - {end_square}
    paths_count = 0
    for square in current_squares:
        if adjacent(square, end_square):
            paths_count += get_paths_count(xmax, ymax, current_squares, square)
    return paths_count


@lru_cache(maxsize = None)
def adjacent(square1, square2):
    x1, y1 = square1
    x2, y2 = square2

    return (abs(x1-x2) == 2 and abs(y1-y2) == 2) or\
        (abs(x1-x2) == 3 and abs(y1-y2) == 0) or\
        (abs(x1-x2) == 0 and abs(y1-y2) == 3)

print(get_solution(6, 4))

# invalid = set([(2,2), (3,0), (0,3), (1,2)])
# print(is_valid(5,5, invalid, (1,2)))
