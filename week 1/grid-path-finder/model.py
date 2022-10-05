import random
import heapq
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    grid[node[0]][node[1]] = value

def get_successors(s):
        directions = []
        directions.append((s[0] + 1, s[1])) # R
        directions.append((s[0] - 1, s[1])) # L
        directions.append((s[0], s[1] - 1)) # D
        directions.append((s[0], s[1] + 1)) # U

        successors = []
        for direction in directions:
            if direction[0] >= 0 and direction[0] < cf.SIZE and direction[1] >= 0 and direction[1] < cf.SIZE and get_grid_value(direction) != 'b':
                successors.append(direction)
        return successors

def UCS(app, start, goal):
    frontier = PriorityQueue()
    visited = set()
    path = {}

    frontier.put(start, get_grid_value(start)) # Start node with cost=0
    visited.add(start)

    while not frontier.empty():
        s = frontier.get()

        if s == goal:
            app.draw_path(path) # Draw dark blue path line
            return path

        visited.add(s)

        for successor in get_successors(s):
            new_cost = get_grid_value(s) + 1
            if successor not in visited or (new_cost < get_grid_value(successor)):
                set_grid_value(successor, new_cost)
                frontier.put(successor, new_cost)
                path[successor] = s
                app.plot_node(s, color=cf.PATH_C)
                app.plot_line_segment(s[0], s[1], successor[0], successor[1], color=cf.PATH_C)
                visited.add(successor)
                app.pause()

def a_star(app, start, goal):
    frontier = PriorityQueue()
    visited = set()
    visited.add(start)
    path = {}
    frontier.put(start, get_grid_value(start)) # Start node with cost=0

    while not frontier.empty():
        s = frontier.get()
        visited.add(s)

        if s == goal:
            app.draw_path(path)
            return path

        def heuristic(start, goal):
            dx = abs(start[0]-goal[0])
            dy = abs(start[1]-goal[1])
            # return dx + dy
            return 2*math.sqrt(dx**2+dy**2) # Diagonal preference
        
        for successor in get_successors(s):
            new_cost = get_grid_value(s) + 1
            if successor not in visited or (new_cost < get_grid_value(successor)):
                    set_grid_value(successor, new_cost) # Set new cost
                    priority = new_cost + heuristic(successor, goal)
                    frontier.put(successor, priority)
                    path[successor] = s
                    app.plot_node(s, color=cf.PATH_C)
                    app.plot_line_segment(s[0], s[1], successor[0], successor[1], color=cf.PATH_C)
                    visited.add(successor)
                    app.pause()
