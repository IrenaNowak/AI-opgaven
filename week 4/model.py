import random
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

#-----------------------------------------------------------------------------
# (x, y) = (0, 0) is the top left of the grid
#
# each  state is encoded as (x, y, action)
# where: 0 <= x <= cf.SIZE - 1,
#        0 <= y <= cf.SIZE - 1,
# and action is one of {'L', 'R', 'U', 'D', 'S'} meaning {'left', 'right', 'up', 'down', 'stay'}.
# note that <action> refers to the previous action
#-----------------------------------------------------------------------------

class Distribution(dict):
    # the Distribution class extends a Python dictionary
    def __missing__(self, key):
        # if the key is missing, return probability 0
        return 0

    def renormalize(self):
        # scale all the probabilities so that they sum to 1
        # this is necessary for positions at/in borders/corners

        normalization_constant = sum(self.values())
        for key in self.keys():
            self[key] /= normalization_constant

def get_all_states():
    # returns a (long) list of all possible states (position and previous action) ex. (7, 7, 'S')
    # we need this in Viterbi (1065 states)
    all_states = []
    for x in range(cf.SIZE):
        for y in range(cf.SIZE):
            possible_prev_actions = ['L', 'R', 'U', 'D', 'S']

            if x == 0: # previous action could not have been to go right
                possible_prev_actions.remove('R')
            if x == cf.SIZE - 1: # could not have gone left
                possible_prev_actions.remove('L')
            if y == 0: # could not have gone down
                possible_prev_actions.remove('D')
            if y == cf.SIZE - 1: # could not have gone up
                possible_prev_actions.remove('U')

            for action in possible_prev_actions:
                all_states.append((x, y, action))
    return all_states

def transition_model(state):
    # given a state (position and previous action), return a dict with keys = possible next states and values = probabilities
    # example: {(7, 7, 'S'): 0.2, (7, 6, 'U'): 0.2, (7, 8, 'down'): 0.2, (6, 7, 'L'): 0.2, (8, 7, 'R'): 0.2}

    x, y, action = state
    distr_next_states = Distribution()

    # we can always stay where we are
    if action == 'S':
        distr_next_states[(x, y, 'S')] = .2
    else:
        distr_next_states[(x, y, 'S')] = .1

    if y > 0: # we can go up
        if action == 'S':
            distr_next_states[(x, y-1, 'U')] = .2
        if action == 'U':
            distr_next_states[(x, y-1, 'U')] = .9
    if y < cf.SIZE - 1: # we can go D
        if action == 'S':
            distr_next_states[(x, y+1, 'down')] = .2
        if action == 'down':
            distr_next_states[(x, y+1, 'down')] = .9
    if x > 0: # we can go left
        if action == 'S':
            distr_next_states[(x-1, y, 'L')] = .2
        if action == 'L':
            distr_next_states[(x-1, y, 'L')] = .9
    if x < cf.SIZE - 1: # we can go right
        if action == 'S':
            distr_next_states[(x+1, y, 'R')] = .2
        if action == 'R':
            distr_next_states[(x+1, y, 'R')] = .9

    # if were at border or in corner then renormalize
    distr_next_states.renormalize()
    return distr_next_states

def get_next_state(distr_next_states):
    pass

def observation_model(state):
    # given a  state, return the Distribution for its observation
    x, y, action    = state
    observed_states = Distribution()

    r = 1
    observed_states[(x, y)] = 1.
    observed_states[(x-r, y)] = 1.
    observed_states[(x+r, y)] = 1.
    observed_states[(x, y-1)] = 1.
    observed_states[(x, y+1)] = 1.

    observed_states.renormalize()
    return observed_states

def Viterbi(start_state, all_possible_states, observations):
    pass

def load_data(filename):
    states = []
    observed_path = []

    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '#':
                continue
            line = line.strip()
            parts = line.split()

            prev_action = parts[0]

            # real position
            string_xy = parts[1].split(',')
            real_x = int(string_xy[0])
            real_y = int(string_xy[1])
            states.append((real_x, real_y, prev_action))

            # observed position
            if parts[2] == 'missing':
                observed_path.append(None)
            else:
                string_xy = parts[2].split(',')
                observed_x = int(string_xy[0])
                observed_y = int(string_xy[1])
                observed_path.append((observed_x, observed_y))

    return states, observed_path

def move_robot (app, start):
    # plot a fully random path for demonstration
    # start[0]=x and start[1]=y
    prev = start
    for i in range(100):
        dir = random.choice(['L', 'R', 'U', 'D'])
        match dir:
            case 'L': current = prev[0]-1, prev[1]
            case 'R': current = prev[0]+1, prev[1]
            case 'D': current = prev[0], prev[1]-1
            case 'U': current = prev[0], prev[1]+1

        # check if new position is valid
        if (current[0] >= 0 and current[0] <= cf.SIZE-1 and current[1] >= 0 and current[1] <= cf.SIZE-1):
            app.plot_line_segment(prev[0], prev[1], current[0], current[1], color=cf.ROBOT_C)
            app.pause()
            app.plot_line_segment(prev[0], prev[1], current[0], current[1], color=cf.PATH_C)
            prev = current
            app.pause()

    app.plot_node(current, color=cf.ROBOT_C)

