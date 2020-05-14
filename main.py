import aStarGraph
import Annealing
import time
import random as rand


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


# Test Algorithm
def algorithmAnalysis(algorithm):
    start_time = time.time()
    return algorithm, time.time() - start_time  # returns the path and time of execution

def main():
    rand.seed(35)
    timeAvoidToll = [0,0]
    timeTakeToll = [0,0,0]

    # Run A* the search algorithm
    print('A* that takes traffic components')
    path, timeTakeToll[0] = algorithmAnalysis(aStarGraph.astar_search(romania_map, 'Arad', 'Bucharest', rand))
    print(path)
    print(timeTakeToll[0])

    print('A* that does not take in traffic components')
    pathNoTolls, timeAvoidToll[0] = algorithmAnalysis(aStarGraph.astar_search_no_components(romania_map, 'Arad', 'Bucharest', rand))
    print(pathNoTolls)
    print(timeAvoidToll[0], "\n")

    # Run the Annealing search algorithm
    print('Annealing that takes traffic components')
    minPath, timeTakeToll[1] = algorithmAnalysis(Annealing.simulated_annealing_full(romania_map, 'Arad', 'Bucharest', rand, schedule=Annealing.exp_schedule()))
    print(minPath)
    print(timeTakeToll[1])

    print('Annealing that does not take in traffic components')
    path, timeTakeToll[0] = algorithmAnalysis(Annealing.simulated_annealing_no_components(romania_map, 'Arad', 'Bucharest', rand, schedule=Annealing.exp_schedule()))
    print(path)
    print(timeTakeToll[0])


# Tell python to run main method
if __name__ == "__main__": main()