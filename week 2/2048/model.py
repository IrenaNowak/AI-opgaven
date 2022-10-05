import random
import itertools
import math
from copy import deepcopy

MAX_DEPTH = 3

def merge_left(b):
    # merge the board left
    # this function is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left
        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accu
        if len(row) == 1:
            return acc + [x]
        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accu, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accu, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]

def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]

def merge_down(b):
    # merge the board downward
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]

# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}

def move_exists(b):
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b):
        for row in b:
            for x, y in zip(row[:-1], row[1:]):
                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                # if same value or an empty cell
                if x == y or x == 0 or y == 0:
                    return True
        return False

    # check horizontally and vertically
    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False

def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b

def play_move(b, direction):
    # get merge functin an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b

def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, cols):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue
            
def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert merge_down(b) == [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [[2, 8, 4, 0], [16, 0, 2, 0], [4, 0, 0, 0], [0, 0, 0, 0]]
    assert (merge_down(b)) == [[0, 0, 0, 0], [2, 0, 0, 0], [16, 0, 4, 0], [4, 8, 2, 0]]
    assert (move_exists(b)) == True
    b = [[32, 64, 2, 16], [8, 32, 16, 2], [4, 16, 8, 4], [2, 8, 4, 2]]
    assert (move_exists(b)) == False
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    for i in range(11):
        add_two_four(b)
        print(b)

def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))

tile_importance = [
    [150, 50, 15, 5],
    [50, 15, 5, 1],
    [15, 5, 1, 0],
    [5, 1, 0, 0]]

def copy_board(b):
    return deepcopy(b)

def get_empty_tiles(b):
    empty_tiles = []
    for y in range(len(b)):
        for x in range(len(b[y])):
            if b[y][x] == 0:
                empty_tiles.append((x, y))
    
    return empty_tiles

# Get children nodes
def get_children_you(b):
    # links rechts boven onder
    children = []

    for direction in MERGE_FUNCTIONS.keys():
        board_copy = copy_board(b)
        move = MERGE_FUNCTIONS[direction](board_copy)

        # alleen als zet kan, het board moet per se veranderen
        if move != b:
            children.append(move) # add move without adding 2/4 afterwards

    return children

def get_children_exp(b):
    # return alle mogelijke tegel generaties, dus met een 2 of 4 op elke plek
    # samen met de kans dat dit zich voordoet
    # [(board, probability)] tuple
    children = []
    empty_tiles = get_empty_tiles(b)

    for empty_tile in empty_tiles:
        for new_tile in [2, 4]:
            board_copy = copy_board(b)
            x = empty_tile[0]
            y = empty_tile[1]
            board_copy[y][x] = new_tile

            if new_tile == 2:
                probability = 0.9 / len(empty_tiles) # kans op 2
                children.append((board_copy, probability))
            else:
                probability = 0.1 / len(empty_tiles) # kans op 4
                children.append((board_copy, probability))

    return children

PLAYER = {
    'YOU': 0,
    'EXP': 1 # return weighted avg of all child nodes' values
}

def calc_score(b):
    global tile_importance
    score = 0
    for y in range(len(b)):
        for x in range(len(b[y])):
            tile_score = b[y][x] * b[y][x] # macht verheffen zodat getal (2*X) zwaarder weegt dan 2 X-getallen
            tile_score *= tile_importance[y][x]
            score += tile_score
    return score

# Expectimax algorithm
def expectimax(node, depth, player):    
    if depth == 0:
        return calc_score(node)

    if player == PLAYER['YOU']:
        max_val = 0
        for child in get_children_you(node):
            max_val = max(max_val, expectimax(child, depth-1, PLAYER['EXP']))
        return max_val

    else: # PLAYER['EXP']
        value = 0
        for child in get_children_exp(node): # kans * score
            value = value + (child[1] * expectimax(child[0], depth-1, PLAYER['YOU'])) # child[1] = probability, child[0] = board
        return value

# Get move with expectimax algorithm
def get_expectimax_move(b):
    max_move = None
    max_score = 0

    for move, func in MERGE_FUNCTIONS.items():
        copied = copy_board(b)
        applied_move = func(copied)
        if applied_move == b:
            continue
        
        score = expectimax(applied_move, MAX_DEPTH, PLAYER['YOU'])
        if score > max_score:
            max_score = score
            max_move = move
    return max_move

"""
def expecitmax(node, depth, player):
    if depth = 0 or node_is_terminal_node:
        return heuristic_value_of_node
    if player == YOU:
        for each child of node:
            value = max(value, expectimax(child, depth-1, MIN))
        return value
    else # player == EXP, return weighted avg of all children nodes' values
        for each child of node:
            value := value + (probability[child] * expectimax(child, depth-1))
        return value
"""

"""
• hou het hoogste nummer in een hoek; --> 150
• zorg ervoor dat hoge nummers in de hoek komen; --> 50
• zorg ervoor dat lege cellen niet in de hoek komen; --> 0
• zorg ervoor dat cellen met gelijke waarden dicht bij elkaar blijven. 
"""