import copy
start_board = [[0, 0, 0, 0, 0, 0, 0, 0, 81], [0, 0, 46, 45, 0, 55, 74, 0, 0], [0, 38, 0, 0, 43, 0, 0, 78, 0], [0, 35, 0, 0, 0, 0, 0, 71, 0], [0, 0, 33, 0, 0, 0, 59, 0, 0], [0, 17, 0, 0, 0, 0, 0, 67, 0], [0, 18, 0, 0, 11, 0, 0, 64, 0], [0, 0, 24, 21, 0, 1, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
N = 9
neighbouring_cells = [(1,0), (0,1), (-1, 0), (0, -1)]

def get_next_clue(current_clue):
    if current_clue != N*N:
        return clue_list[clue_list.index(current_clue)+1]
    return N*N

def valid_path(position, stepcount, next_clue_in_list):
    row, col = position

    if stepcount == next_clue_in_list and board[row][col] == next_clue_in_list:
        return True
    elif board[row][col] == 0 and stepcount < next_clue_in_list:
        return True

    if stepcount == 1:
        return True

    return False

def puzzle_complete(position, stepcount):
    row, col = position
    for board_row in board:
        if 0 in board_row:
            return False

    if board[row][col] == stepcount:
        return True
    else:
        return False

def neighbours(position):
    all_neighbours = []
    for row_offset, col_offset in neighbouring_cells:
        new_row = (position[0] + row_offset)
        new_col = (position[1] + col_offset)

        if 0 <= new_row < N and 0 <= new_col < N:
            all_neighbours.append([new_row, new_col])

    return all_neighbours

def solve(position, stepcount, next_clue_in_list, path=[]):
    row, col = position
    path = path + [position]

    if valid_path(position, stepcount, next_clue_in_list):
        board[row][col] = stepcount
        if puzzle_complete(position, stepcount):
            return True
        if stepcount == next_clue_in_list:
            next_clue_in_list = get_next_clue(next_clue_in_list)
    else:
        return False

    for move in neighbours(position):
        if move not in path:
            solved = solve(move, stepcount+1, next_clue_in_list, path)
            if not solved:
                board[move[0]][move[1]] = start_board[move[0]][move[1]]
            else:
                return True

# Find 1 in board and make sorted list of clues
clue_list = [1]
for i in range(N):
    for j in range(N):
        if start_board[i][j] == 1:
            start_position = [i, j]
        elif start_board[i][j] != 0:
            clue_list.append(start_board[i][j])

    if 1 in start_board[i]:
        start_position = [i, start_board[i].index(1)]

clue_list.sort()
board = copy.deepcopy(start_board)

solve(start_position, 1, get_next_clue(1))
for e in board:
    print(e)