import main
import math
import components
import random as rand


# This class represent a node
class Node:
    # Initialize the class
    def __init__(self, name: str, parent: str):
        self.name = name
        self.parent = parent

        self.speedLimit = 0

        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name

    # Sort nodes
    def __lt__(self, other):
        return self.f < other.f

    # Print node
    def __repr__(self):
        return '({0},{1})'.format(self.position, self.f)


# A* search
# def astar_search(graph, heuristics, start, end):
def astar_search(graph, start, end, avoidTolls):
    # Create lists for discovered and visited nodes
    open = []
    closed = []
    # TODO this is the seed to create sudo randomness
    # help to create a more consistent randomness
    rand.seed(999)
    rand.seed(35)
    # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)

    # Add the start node
    open.append(start_node)

    # Loop until the open list is empty
    while len(open) > 0:
        # Sort the open list to get the node with the lowest cost first
        open.sort()

        # Get the node with the lowest cost
        current_node = open.pop(0)

        # Add the current node to the closed list
        closed.append(current_node)

        # Check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name + ': ' + str(current_node.g))
                current_node = current_node.parent
            path.append(start_node.name + ': ' + str(start_node.g))
            # Return reversed path
            return path[::-1]

        # Get neighbours
        neighbors = graph.get(current_node.name)


        # Loop neighbors
        for key, value in neighbors.items():

            # Create a neighbor node

            neighbor = Node(key, current_node)

            # Check if the neighbor is in the closed list
            if (neighbor in closed):
                continue

            # Calculate full path cost
            neighbor.g = graph.get(current_node.name, neighbor.name) + heuristicFunction(neighbor.name, goal_node.name)

            # Calculate full path cost with realistic components that affect
            neighbor.h = components.componentAdjustments(rand, neighbor.g)

            neighbor.f = neighbor.g + neighbor.h

            # Check if neighbor is in open list and if it has a lower f value
            if (add_to_open(open, neighbor) == True and components.tollsComponent(rand.randint(0, 1), avoidTolls)):
                # Everything is green, add neighbor to open list
                open.append(neighbor)

    # Return None, no path is found without tolls
    return "There is no toll-free path to reach the destination."


# Check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True


def heuristicFunction(current, goal):
    x1, y1 = (main.romania_map.locations.get(current))

    x2, y2 = (main.romania_map.locations.get(goal))

    x = int(x2) - int(x1)
    y = int(y2) - int(y1)
    return int(math.sqrt((x ** 2) + (y ** 2)))