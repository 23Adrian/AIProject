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
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent

        seed(len(name))
        num = randint(1,11)
        print(num)
        self.speedLimit = setSpeedLimit(num)
        self.trafficSlowdown = setTrafficSlowdown(num)
        self.trafficAccident = setTrafficAccident(num)
        self.trafficMultiplier = setSpeedLimit(num) * setTrafficAccident(num) * setTrafficSlowdown(num)

        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name

    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f

    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))


def setTrafficSlowdown(randNum):
    switch = {
        1: 1, 2: 1, 3: 1, 4: 1.5, 5: 1.5, 6: 2, 7: 2, 8: 2.5, 9: 2.5, 10: 3,}
    return switch.get(randNum, "Invalid argument")

def setTrafficAccident(randNum):
    switch = {
        1: 1, 2: 1, 3: 1, 4: 1, 5: 4, 6: 1, 7: 1, 8: 4, 9: 1, 10: 1,}
    return switch.get(randNum, "Invalid argument")

def setSpeedLimit(randNum):
    switch = {
        1: 1, 2: 2, 3: 1, 4: 4, 5: 4, 6: 1.35, 7: 1, 8: .80, 9: 1, 10: 1,}
    return switch.get(randNum, "Invalid argument")
