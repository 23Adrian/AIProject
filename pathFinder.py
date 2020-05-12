# Search Algorithms 
from aStarGraph import astar_search
from MinSpanSearch import MinSpanSearch

# Utility
import time
from graph import Graph


# Map
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
def algorithmAnalysis(algo):
    start_time = time.time()
    print(start_time)
    return algo, time.time() - start_time  # returns the path and time of execution


# The main entry point for this module
def main():
    # Run the search algorithm
    algorithm1 = algorithmAnalysis(astar_search(romania_map,  'Arad', 'Bucharest', True))
    algorithm2 = algorithmAnalysis(MinSpanSearch(romania_map,  'Arad', 'Bucharest'))
    print("Algorithm 1:\nRuntime: {}\npath: {}".format(algorithm1[1], algorithm1[0]))
    print("Algorithm 2:\nRuntime: {}\npath: {}".format(algorithm2[1], algorithm2[0]))
    if algorithm1[1] == algorithm2[1]:
        print("Both algorithms took the same time to execute")
    elif algorithm1[1] > algorithm2[1]:
        print("A* algorithm was faster")
    else:
        print("Algorithm 2 was faster")


# Tell python to run main method
if __name__ == "__main__": main()
