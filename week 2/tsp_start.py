import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed() # the current system time is used as a seed
                  # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-') # blue circle markers, solid line style
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

def nn(cities):
    # Initialize all vertices as unvisited
    unvisited = set(cities)

    # Start at a city
    current = unvisited.pop()

    # Path
    tour = [current]

    while len(unvisited) > 0:
        # Find nearest neighbor of current
        nearest = City(x = math.inf, y = math.inf) # High distance
        for city in unvisited:
            if distance(current, city) < distance(current, nearest):
                nearest = city
        tour.append(nearest)
        current = nearest
        unvisited.remove(nearest)
    
    return tour

def two_opt(cities):
    tour = nn(cities)

    """
    repeat until no improvement is made {
        best_distance = calculateTotalDistance(existing_route)
        start_again:
        for (i = 0; i <= number of nodes eligible to be swapped - 1; i++) {
            for (j = i + 1; j <= number of nodes eligible to be swapped; j++) {
                new_route = 2optSwap(existing_route, i, j)
                new_distance = calculateTotalDistance(new_route)
                if (new_distance < best_distance) {
                    existing_route = new_route
                    best_distance = new_distance
                    goto start_again
                }
            }
        }
    }
    """

    # Repeat until no improvement is made
    improved = True
    while improved:
        best_distance = tour_length(tour)
        improved = False
        for i in range(len(tour) - 1):
            for j in range(i + 1, len(tour)):
                new_route = two_opt_swap(tour, i, j)
                new_distance = tour_length(new_route)
                if(new_distance < best_distance):
                    tour = new_route
                    best_distance = new_distance
                    improved = True
                    
    return tour

def two_opt_swap(existing, i, j):
    return existing[:i] + list(reversed(existing[i:j])) + existing[j:]

# plot_tsp(nn, make_cities(500))
plot_tsp(two_opt, make_cities(200))
