from graph import *
from collections import defaultdict
import components
import heapq
import random as rand


def create_spanning_tree(graph, starting_vertex):
    mst = defaultdict(set)
    visited = set([starting_vertex])
    edges = [
        (cost, starting_vertex, to)
        for to, cost in graph[starting_vertex].items()
    ]
    heapq.heapify(edges)

    while edges:
        cost, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst[frm].add(to)
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    heapq.heappush(edges, (cost, to, to_next))
    return mst


example_graph = {
    'A': {'B': 2, 'C': 3},
    'B': {'A': 2, 'C': 1, 'D': 1, 'E': 4},
    'C': {'A': 3, 'B': 1, 'F': 5},
    'D': {'B': 1, 'E': 1},
    'E': {'B': 4, 'D': 1, 'F': 1},
    'F': {'C': 5, 'E': 1, 'G': 1},
    'G': {'F': 1},
}

dict(create_spanning_tree(example_graph, 'A'))
def MinSpanSearch(graph, start, end, avoidTolls):
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
            neighbor.g = graph.get(current_node.name, neighbor.name) 

            # Calculate full path cost with realistic components that affect
            neighbor.h = components.componentAdjustments(rand, neighbor.g)


            neighbor.f = neighbor.g + neighbor.h

            # Check if neighbor is in open list and if it has a lower f value
            if (add_to_open(open, neighbor) == True and components.tollsComponent(rand.randint(0, 1), avoidTolls)):
                # Everything is green, add neighbor to open list
                open.append(neighbor)

    # Return None, no path is found without tolls
    return "There is no toll-free path to reach the destination."

def add_to_open(open, neighbor):
    for node in open:
        if(neighbor == node and neighbor.f> node.f):
            return False
    return True