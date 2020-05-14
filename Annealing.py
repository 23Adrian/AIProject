from SearchAlgos import GraphProblem
import components
import math
import main
from graph import Graph, Node
from utils import probability
import numpy as np
import sys


class GraphProblemStochastic(GraphProblem):
    """
    A version of GraphProblem where an action can lead to
    nondeterministic output i.e. multiple possible states.
    Define the graph as dict(A = dict(Action = [[<Result 1>, <Result 2>, ...], <cost>], ...), ...)
    A the dictionary format is different, make sure the graph is created as a directed graph.
    """
    def result(self, state, action):
        return self.graph.get(state, action)

    def path_cost(self):
        raise NotImplementedError


def exp_schedule(k=20, lam=0.005, limit=50):
    """One possible schedule function for simulated annealing"""
    return lambda t: (k * np.exp(-lam * t) if t < limit else 0)


def choose(neighbors_list,rand):
    choice = rand.randrange(len(neighbors_list))
    return neighbors_list[choice]

def simulated_annealing_no_components(graph, start,goal,rand, schedule):
    states = []
    start_node = Node(start, None)
    current = Node(start, None)

    for t in range(sys.maxsize):
        states.append(current.name)
        T = schedule(t)
        if T == 0:
            path = []
            while current != start_node:
                path.append(current.name + ': ' + str(current.f))
                current = current.parent
            path.append(start_node.name + ': ' + str(start_node.f))
            # Return reversed path
            return path[::-1]
            # return states
        neighbors = graph.get(current.name)
        if not neighbors:
            return current.name
        next_choice = Node(choose(list(neighbors),rand), current)

        # Calculates path cost without realistic components
        current.f = heuristicFunction(str(current.name), goal)
        next_choice.f = heuristicFunction(str(next_choice.name), goal)
        # calcualtes delta e with the path costs
        delta_e = current.f - next_choice.f
        if delta_e > 0 or probability(np.exp(delta_e / T)):
            current = next_choice


def simulated_annealing_full(graph, start, goal, rand, schedule=exp_schedule()):
    """ This version returns all the states encountered in reaching 
    the goal state."""
    states = []
    start_node = Node(start,None)
    current = Node(start, None)

    for t in range(sys.maxsize):
        states.append(current.name)
        T = schedule(t)
        if T == 0:
            path = []
            while current != start_node:
                path.append(current.name + ': ' + str(current.f))
                current = current.parent
            path.append(start_node.name + ': ' + str(start_node.f))
            # Return reversed path
            return path[::-1]
            #return states
        neighbors = graph.get(current.name)
        if not neighbors:
            return current.name
        next_choice = Node(choose(list(neighbors),rand), current)

        # Calculates path cost with realistic components
        current.f = components.componentAdjustments(rand, heuristicFunction(str(current.name), goal))
        next_choice.f = components.componentAdjustments(rand, heuristicFunction(str(next_choice.name), goal))

        # calcualtes delta e with the path costs
        delta_e = current.f - next_choice.f
        if delta_e > 0 or probability(np.exp(delta_e / T)):
            current = next_choice


def heuristicFunction(current, goal):
    x1, y1 = (main.romania_map.locations.get(current))

    x2, y2 = (main.romania_map.locations.get(goal))

    x = int(x2) - int(x1)
    y = int(y2) - int(y1)
    return int(math.sqrt((x ** 2) + (y ** 2)))


