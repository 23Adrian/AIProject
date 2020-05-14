from SearchAlgos import GraphProblem
import math
import main
from graph import Graph,Node
from utils import probability
import numpy as np
from random import randrange,seed,random
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


def choose(neighbors_list):
    choice = randrange(len(neighbors_list))
    return neighbors_list[choice]


def simulated_annealing_full(graph, start, goal, schedule=exp_schedule()):
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
                # Borrar este comentario, se necesita que current.g marque el valor verdadero una vez se haga lo de accidents, etc
                path.append(current.name + ': ' + str(current.g))
                current = current.parent
            path.append(start_node.name + ': ' + str(start_node.g))
            # Return reversed path
            print(states)
            return path[::-1]
            #return states
        neighbors = graph.get(current.name)
        if not neighbors:
            return current.name
        next_choice = Node(choose(list(neighbors)), current)
        delta_e = heuristicFunction(str(current.name), goal) - heuristicFunction(str(next_choice.name), goal)
        if delta_e > 0 or probability(np.exp(delta_e / T)):
            current = next_choice


def and_or_graph_search(problem):
    """[Figure 4.11]Used when the environment is nondeterministic and completely observable.
    Contains OR nodes where the agent is free to choose any action.
    After every action there is an AND node which contains all possible states
    the agent may reach due to stochastic nature of environment.
    The agent must be able to handle all possible states of the AND node (as it
    may end up in any of them).
    Returns a conditional plan to reach goal state,
    or failure if the former is not possible."""

    # functions used by and_or_search
    def or_search(state, problem, path):
        """returns a plan as a list of actions"""
        if problem.goal_test(state):
            return []
        if state in path:
            return None
        for action in problem.actions(state):
            plan = and_search(problem.result(state, action),
                              problem, path + [state, ])
            if plan is not None:
                return [action, plan]

    def and_search(states, problem, path):
        """Returns plan in form of dictionary where we take action plan[s] if we reach state s."""
        plan = {}
        for s in states:
            plan[s] = or_search(s, problem, path)
            if plan[s] is None:
                return None
        return plan

    # body of and or search
    return or_search(problem.initial, problem, [])


def heuristicFunction(current, goal):
    x1, y1 = (main.romania_map.locations.get(current))

    x2, y2 = (main.romania_map.locations.get(goal))

    x = int(x2) - int(x1)
    y = int(y2) - int(y1)
    return int(math.sqrt((x ** 2) + (y ** 2)))


