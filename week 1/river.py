import copy

state = [['F', 'G', 'C', 'W'], []] # Farmer, goat, cabbage, wolf

# Check if farmer is on left or right side of the river
def farmer_left(state):
    return "F" in state[0]

# Get current state as a string
def state_to_string(state):
    return ''.join(state[0]) + "|" + ''.join(state[1])

# Check if WG and GC aren't on the same side without F
def state_is_valid(state):
    if farmer_left(state):
        if "G" in state[1] and "W" in state[1]: #F|GW
            return False
        elif "G" in state[1] and "C" in state[1]: #F|GC
            return False
    
    else:
        if "G" in state[0] and "W" in state[0]: #GW|F
            return False
        elif "G" in state[0] and "C" in state[0]: #GC|F
            return False

    return True

# Check if goal state has been reached
def is_goal(state):
    return len(state[0]) == 0

# Cross the river, farmer can bring 0 or 1 item to the other side of river
def cross_river(state, bringing = None):
    if farmer_left(state):
        from_side = state[0]
        to_side = state[1]
    else:
        from_side = state[1]
        to_side = state[0]

    from_side.remove("F")
    to_side.append("F")

    if bringing is not "F": # Farmer can't bring himself with him
        from_side.remove(bringing)
        to_side.append(bringing)

    return state

# Get list of successor nodes
def get_children(state):
    # state.sort()
    children = []

    for i in state[0] if farmer_left(state) else state[1]:
        checking = cross_river(copy.deepcopy(state), i) # Check if next node is valid // use copy of state just in case because don't want to make the real move yet
        if state_is_valid(checking):
            children.append(checking)

    return children

# Depth first search algorithm
def dfs(state, path = []):
    path = path + [state_to_string(state)] # Path traversed

    if is_goal(state): # Check if goal state has been reached + return correct path
        return [path]

    all_paths = [] # Collect all possible paths

    # Find paths, traverse through the children nodes
    for child in get_children(state):
        if state_to_string(child) not in path:
            new_paths = dfs(child, path)
            # Add every path that has been found to all_paths
            for new_path in new_paths:
                all_paths.append(new_path)

    return all_paths

# Print all possible paths
for path in (dfs(state)):
    print(path)