import random, string, pprint

# Create N*N board, 2D array coordinates
def create_boggle_board(n):
    return [[random.choice(string.ascii_lowercase)for x in range(n)] for y in range(n)]

def solve_nl():
    return open("week 1/boggle/words_NL.txt", "r", encoding = "ISO-8859-1")

def solve_en():
    return open("week 1/boggle/words_EN.txt", "r", encoding = "ISO-8859-1")

# Trie structure
# {
#     'i': {
#         {'q': {}},
#         {'t': {}}
#     }
# }

# Build trie of words from file
def create_trie(f):
    trie = {} # Start with empty dict

    for line in f:
        word = line.strip()
        temp_trie = trie
        for letter in word:
            temp_trie = temp_trie.setdefault(letter, {}) # After each letter a new, empty dict
        temp_trie = temp_trie.setdefault('END', 'END') # END at the end of a word

    return trie

# Left in the grid
def left(row):
    return (row - 1) % N # % N otherwise list index out of range

# Right in the grid
def right(row):
    return (row + 1) % N

# Up in the grid
def up(col):
    return (col - 1) % N

# Down in the grid
def down(col):
    return (col + 1) % N

N = 4
TRIE = create_trie(solve_nl())
BOARD = create_boggle_board(N)
WORDS = []

# Board uses [row][col], [0][0] upper left corner
def dfs(row, col, prefix, trie, prev_row, prev_col):
    letter = BOARD[row][col]
    word = prefix + letter

    if letter in trie.keys():
        if 'END' in trie[letter].keys(): # Word ends with END so a word is found if this key is reached
            if word not in WORDS: # No duplicate words
                WORDS.append(word)
        if row != prev_row or right(row) != prev_row: # Right neighbor
            dfs(right(row), col, word, trie[letter], row, col)
        if row != prev_row or left(row) != prev_row: # Left neighbor
            dfs(left(row), col, word, trie[letter], row, col)
        if col != prev_col or up(col) != prev_col: # Up neighbor
            dfs(row, up(col), word, trie[letter], row, col)
        if col != prev_col or down(col) != prev_col: # Down neighbor
            dfs(row, down(col), word, trie[letter], row, col)

# Function to find words using DFS
def find_words():
    for row in range(N):
        for col in range(N):
            dfs(row, col, '', TRIE, -1, -1)
    
    if not WORDS:
        return "No words found"

    return WORDS

pprint.pprint(BOARD)
print("WORDS FOUND:")
print(find_words())