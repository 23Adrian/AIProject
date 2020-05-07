
import time
from graphics import *

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        #distance between node and start
        self.g = 0
        #heuristic to reach
        self.h = 0
        #total cost of node
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position



def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    discovered = []
    visited = []

    # Add the start node
    discovered.append(start_node)

    # Loop until you find the end
    while len(discovered) > 0:

        # Get the current node
        current_node = discovered[0]
        current_index = 0

        for index, item in enumerate(discovered):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        discovered.pop(current_index)
        visited.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            #walk back to the root node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in visited:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            #heuristic is pythagorean theorem to the goal
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            #  to see if the child is already discovered
            for open_node in discovered:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            discovered.append(child)


def main():



    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    begin = time.time()
    start = (0, 0)
    end = (7, 6)

    path = astar(maze, start, end)
    finish = time.time()
    totalTime = finish-begin
    print(path)
    print("elapsed time = ")
    print(totalTime)


if __name__ == '__main__':
    main()