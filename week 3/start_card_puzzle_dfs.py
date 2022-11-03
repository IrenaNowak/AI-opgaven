import itertools
from math import perm

'''
Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other
'''
# the board has 8 cells, let’s represent the board with a dict key=cell, value=card
start_board = {cell: '.' for cell in range(8)}
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbors = {0:[3], 1:[2], 2:[1,4,3], 3:[0,2,5], 4:[2,5], 5:[3,4,6,7], 6:[5], 7:[5]}

def is_valid(board):
    
    used_cards = {'K': 0, 'Q': 0, 'J': 0, 'A': 0}

    for i, cell in board.items() if type(board) is dict else enumerate(board):
        if cell == '.': # Cell should not be empty
            continue

        # Dupe count, every card may only be used twice
        used_cards[cell] += 1
        if used_cards[cell] > 2:
            return False

        card_neighbors = [board[j] for j in neighbors[i]]

        # No two of the same cards border each other
        if cell in card_neighbors:
            return False
        
        # Ace borders king & no Ace borders Queen
        if cell == "A":
            if "Q" in card_neighbors or ("K" not in card_neighbors and "." not in card_neighbors):
                return False

        # Every King borders Queen
        if cell == "K":
            if "Q" not in card_neighbors and "." not in card_neighbors:
                return False

        # Every Queen borders Jack & no Ace borders Queen
        if cell == "Q":
            if "A" in card_neighbors or ("J" not in card_neighbors and "." not in card_neighbors):
                return False

    return True

def brute_force_solve():
    count_permutations = 0

    for permutation in itertools.permutations(cards):
    # for permutation in set(itertools.permutations(cards)):
        count_permutations += 1
        
        if is_valid(permutation):             
            return print("Total permutations brute force: {}".format(count_permutations))

def dfs_backtracking_solve(board):
    global count
    count += 1
    if is_valid(board):
        if "." not in board.values(): # If all keys have value
            print("Solution {}".format(board))
            print("Count {}".format(count))
            return True

        # Select next key in dict
        next = None
        for k, v in board.items():
            if v == ".":
                next = k
                break

        for card in ['K', 'Q', 'J', 'A']: # Unique cards
            board[next] = card

            if dfs_backtracking_solve(board):
                return True # Found a solution
            else:
                board[next] = "." # Undo assignment

    return False

def test():
    # is_valid(board) checks all cards, returns False if any card is invalid
    print('f ',is_valid({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}))
    print('f ',is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))
    print('t ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('t ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'})) # [1]
    print('f ',is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'})) # [3]
    print('t ',is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'})) # [3] 
    print('f ',is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'})) # [3]
    print('f ',is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'})) # [4]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'})) # [5]
    print('f ',is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'})) # [5]
    print('t ',is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))

test()

brute_force_solve()

count = 0
dfs_backtracking_solve(start_board)


"""
Backtracking search
def solve(dict):                        # Dict represents a tree variable:value
    if all tests pass:                  # All constraints are satisfied
        if all keys have a value:
            print solution
            return True
        select next key in dict
        for all values in v domain:     # Try them all
            dict[key] = v               # Assign value to variable
            if solve(dict):
                return True             # Found a solution
            dict[key] = empty_value     # Undo assignment
    return False                        # Didn't find solution
"""