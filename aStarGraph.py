import math
from random import seed, randint


class Graph:
    # Initialize the class
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    # Create an undirected graph by adding symmetric edges
    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist

    # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance

    # Get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    # Return a list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)


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
    seed(999)
    seed(35)
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
            neighbor.h = trafficComponent(randint(0, 5)) + \
                         speedComponent(randint(0, 4), neighbor.g) + \
                         accidentComponent(randint(0, 1))

            neighbor.f = neighbor.g + neighbor.h

            # Check if neighbor is in open list and if it has a lower f value
            if (add_to_open(open, neighbor) == True and tollsComponent(randint(0, 1), avoidTolls)):
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
    x1, y1 = (romania_map.locations.get(current))

    x2, y2 = (romania_map.locations.get(goal))

    x = int(x2) - int(x1)
    y = int(y2) - int(y1)
    return int(math.sqrt((x ** 2) + (y ** 2)))


# heuristic based on traffic
def trafficComponent(traffic):
    # no traffic
    if traffic == 0:
        return 0
    # little traffic
    if traffic == 1:
        return 20
    # light traffic
    if traffic == 2:
        return 30
    # medium traffic
    if traffic == 3:
        return 60
    # big traffic
    if traffic == 4:
        return 120
    # heavy traffic
    return 200


# heuristic based on speed limit
def speedComponent(speed, distance):
    # 60mph base case
    if speed == 0:
        return 0
    # 30mph
    if speed == 1:
        return distance * 2
    # 15mph
    if speed == 2:
        return distance * 4
    # 45mph
    if speed == 3:
        return int(distance * 1.333)
    # 75mph
    return int(distance * .80)


def accidentComponent(accident):
    # no accident
    if accident == 0:
        return 0
    return 50


def tollsComponent(toll, avoidTolls):
    # has toll and the user want to avoid tolls
    if (toll == 1 and avoidTolls == True):
        return False
    return True


def UndirectedGraph(graph_dict=None):
    """Build a Graph where every edge (including future ones) goes both ways."""
    return Graph(graph_dict=graph_dict, directed=False)


romania_map = UndirectedGraph(dict(
    Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    Drobeta=dict(Mehadia=75),
    Eforie=dict(Hirsova=86),
    Fagaras=dict(Sibiu=99),
    Hirsova=dict(Urziceni=98),
    Iasi=dict(Vaslui=92, Neamt=87),
    Lugoj=dict(Timisoara=111, Mehadia=70),
    Oradea=dict(Zerind=71, Sibiu=151),
    Pitesti=dict(Rimnicu=97),
    Rimnicu=dict(Sibiu=80),
    Urziceni=dict(Vaslui=142)))

romania_map.locations = dict(
    Arad=(91, 492), Bucharest=(400, 327), Craiova=(253, 288),
    Drobeta=(165, 299), Eforie=(562, 293), Fagaras=(305, 449),
    Giurgiu=(375, 270), Hirsova=(534, 350), Iasi=(473, 506),
    Lugoj=(165, 379), Mehadia=(168, 339), Neamt=(406, 537),
    Oradea=(131, 571), Pitesti=(320, 368), Rimnicu=(233, 410),
    Sibiu=(207, 457), Timisoara=(94, 410), Urziceni=(456, 350),
    Vaslui=(509, 444), Zerind=(108, 531))


# The main entry point for this module
def main():
    # Run the search algorithm
    #this will continue even if it has tolls
    path = astar_search(romania_map, 'Arad', 'Bucharest', False)
    #this will avoid tolls into account tolls
    pathNoTolls = astar_search(romania_map, 'Arad', 'Bucharest', True)
    print(path)
    print(pathNoTolls)


# Tell python to run main method
if __name__ == "__main__": main()
