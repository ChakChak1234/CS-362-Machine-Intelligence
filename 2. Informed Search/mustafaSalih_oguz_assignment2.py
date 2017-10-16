import copy
import math
from Queue import PriorityQueue
from collections import deque

class Node:
    def __init__(self, point, parent=None):
        self.point = point
        self.parent = parent

def get_successors(initial_state):
    """Successor function for the block world puzzle
       Parameters
       ----------
       initial_state: 2-dimensional array representing initial block world config
       Returns
       -------
       expanded_states: type - list of 2D arrrays
    """
    expanded_states = []
    first = (-1, -1)
    second = (-1, -1)
    # find empty places
    for i in range(len(initial_state)):
        for j in range(len(initial_state)):
            if initial_state[i][j] == 0:
                if first == (-1, -1):
                    first = (i, j)
                else:
                    second = (i, j)
                    break

    # find single blocks and add successors
    for single in [first, second]:
        if single[0] % 3 == 0 and single[1] % 3 == 0:  # corners with only two neighbors
            if single[0] == 0:  # single row
                if initial_state[single[0] + 1][single[1]] == 1:  # one below is single block
                    get_neighbor(expanded_states, initial_state, single[0], single[1], single[0] + 1, single[1])
            else:  # last row
                if initial_state[single[0] - 1][single[1]] == 1:  # one up is single block
                    get_neighbor(expanded_states, initial_state, single[0], single[1], single[0] - 1, single[1])
            if single[1] == 0:  # single column
                if initial_state[single[0]][single[1] + 1] == 1:  # one right is single block
                    get_neighbor(expanded_states, initial_state, single[0], single[1], single[0], single[1] + 1)
            else:  # last column
                if initial_state[single[0]][single[1] - 1] == 1:  # one left is single block
                    get_neighbor(expanded_states, initial_state, single[0], single[1], single[0], single[1] - 1)
        elif single[0] == single[1] or single == (2, 1) or single == (1, 2):  # non corner places with four neighbors
            if initial_state[single[0] + 1][single[1]] == 1:  # one below is single block
                get_neighbor(expanded_states, initial_state, single[0], single[1], single[0] + 1, single[1])
            if initial_state[single[0] - 1][single[1]] == 1:  # one up is single block
                get_neighbor(expanded_states, initial_state, single[0], single[1], single[0] - 1, single[1])
            if initial_state[single[0]][single[1] + 1] == 1:  # one right is single block
                get_neighbor(expanded_states, initial_state, single[0], single[1], single[0], single[1] + 1)
            if initial_state[single[0]][single[1] - 1] == 1:  # one left is single block
                get_neighbor(expanded_states, initial_state, single[0], single[1], single[0], single[1] - 1)
        else:   # non corner places with three neighbors
            if single[0] != 3 and initial_state[single[0] + 1][single[1]] == 1:  # one below is single block
                get_neighbor(expanded_states, initial_state, single[0], single[1], single[0] + 1, single[1])
            if single[0] != 0 and initial_state[single[0] - 1][single[1]] == 1:  # one up is single block
                get_neighbor(expanded_states, initial_state, single[0], single[1], single[0] - 1, single[1])
            if single[1] != 3 and initial_state[single[0]][single[1] + 1] == 1:  # one right is single block
                get_neighbor(expanded_states, initial_state, single[0], single[1], single[0], single[1] + 1)
            if single[1] != 0 and initial_state[single[0]][single[1] - 1] == 1:  # one left is single block
                get_neighbor(expanded_states, initial_state, single[0], single[1], single[0], single[1] - 1)

    # find double blocks
    doubles = []
    for i in range(len(initial_state)):
        for j in range(len(initial_state)):
            if initial_state[i][j] == 2:
                neighbor = (-1,-1)
                if i % 3 == 0 and j % 3 == 0:  # corners with only two neighbors
                    if i == 0:  # single row
                        if initial_state[i + 1][j] == 2 and [(i+1,j),(i,j)] not in doubles:  # one below is double block
                            doubles.append([(i,j),(i+1,j)])
                    else:  # last row
                        if initial_state[i - 1][j] == 2 and [(i-1,j),(i,j)] not in doubles:  # one up is double block
                            doubles.append([(i, j), (i - 1, j)])
                    if j == 0:  # single column
                        if initial_state[i][j + 1] == 2 and [(i,j+1),(i,j)] not in doubles:  # one right is double block
                            doubles.append([(i, j), (i, j+1)])
                    else:  # last column
                        if initial_state[i][j - 1] == 2 and [(i,j-1),(i,j)] not in doubles:  # one left is single block
                            doubles.append([(i, j), (i, j-1)])
                elif i == j or (i,j) == (2, 1) or (i,j) == (1, 2):  # non corner places with four neighbors
                    if initial_state[i + 1][j] == 2 and [(i + 1, j), (i, j)] not in doubles:  # one below is double block
                        doubles.append([(i, j), (i + 1, j)])
                    if initial_state[i - 1][j] == 2 and [(i - 1, j), (i, j)] not in doubles:  # one up is double block
                        doubles.append([(i, j), (i - 1, j)])
                    if initial_state[i][j + 1] == 2 and [(i, j + 1), (i, j)] not in doubles:  # one right is double block
                        doubles.append([(i, j), (i, j + 1)])
                    if initial_state[i][j - 1] == 2 and [(i, j - 1), (i, j)] not in doubles:  # one left is single block
                        doubles.append([(i, j), (i, j - 1)])
                else:  # non corner places with three neighbors
                    if i != 3 and initial_state[i + 1][j] == 2 and [(i + 1, j), (i, j)] not in doubles:  # one below is double block
                        doubles.append([(i, j), (i + 1, j)])
                    if i != 0 and initial_state[i - 1][j] == 2 and [(i - 1, j), (i, j)] not in doubles:  # one up is double block
                        doubles.append([(i, j), (i - 1, j)])
                    if j != 3 and initial_state[i][j + 1] == 2 and [(i, j + 1), (i, j)] not in doubles:  # one right is double block
                        doubles.append([(i, j), (i, j + 1)])
                    if j != 0 and initial_state[i][j - 1] == 2 and [(i, j - 1), (i, j)] not in doubles:  # one left is single block
                        doubles.append([(i, j), (i, j - 1)])

    # remove wrong pieces

    if len(doubles) == 3:
        if (doubles[0][0] in doubles[1] or doubles[0][0] in doubles[2]) and (doubles[0][1] in doubles[1] or doubles[0][1] in doubles[2]):
            doubles.pop(0)
        elif (doubles[1][0] in doubles[0] or doubles[1][0] in doubles[2]) and (doubles[1][1] in doubles[0] or doubles[1][1] in doubles[2]):
            doubles.pop(1)
        elif (doubles[2][0] in doubles[0] or doubles[2][0] in doubles[1]) and (doubles[2][1] in doubles[0] or doubles[2][1] in doubles[1]):
            doubles.pop(2)

    # move doubles
    for double in doubles:
        x1 = double[0][0]
        y1 = double[0][1]
        x2 = double[1][0]
        y2 = double[1][1]

        if x1!=x2:
            horizontal = False
        else:
            horizontal = True

        #   x1
        #   x2

        # x1 x2
        if x2 != 3:  # not last row
            if initial_state[x2+1][y2] == 0:  # get below
                if initial_state[x1+1][y1] == 0:  # horizontal
                    get_double_neighbor(expanded_states, initial_state, x1, y1, x1+1, y1, x2, y2, x2+1, y2)
                elif not horizontal:  # vertical
                    get_neighbor(expanded_states, initial_state, x1, y1, x1+2, y1)
        if x1 != 0:  # not first row
            if initial_state[x1-1][y1] == 0:  # get up
                if initial_state[x2-1][y2] == 0:  # horizontal
                    get_double_neighbor(expanded_states, initial_state, x1, y1, x1-1, y1, x2, y2, x2-1, y2)
                elif not horizontal:  # vertical
                    get_neighbor(expanded_states, initial_state, x1, y1, x1-2, y1)
        if y1 != 0:  # not first column
            if initial_state[x1][y1-1] == 0:  # get left
                if initial_state[x2][y2-1] == 0:  # vertical
                    get_double_neighbor(expanded_states, initial_state, x1, y1, x1, y1-1, x2, y2, x2, y2-1)
                elif horizontal:  # horizontal
                    get_neighbor(expanded_states, initial_state, x1, y1, x1, y1-2)
        if y2 != 3:  # not last column
            if initial_state[x2][y2+1] == 0:  # get right
                if initial_state[x1][y1+1] == 0:  # vertical
                    get_double_neighbor(expanded_states, initial_state, x1, y1, x1, y1+1, x2, y2, x2, y2+1)
                elif horizontal:  # horizontal
                    get_neighbor(expanded_states, initial_state, x1, y1, x1, y1+2)

    # find quadruples
    quad = []
    for i in range(len(initial_state)):
        for j in  range(len(initial_state)):
            if initial_state[i][j] == 4:
                quad.append((i,j))
    if quad == [(0, 2), (1, 3), (2, 2), (3, 2)]:
        print initial_state
    x1 = quad[0][0]
    y1 = quad[0][1]
    x2 = quad[3][0]
    y2 = quad[3][1]
    x3 = quad[1][0]
    y3 = quad[1][1]
    x4 = quad[2][0]
    y4 = quad[2][1]

    # x1 x3
    # x4 x2

    if x2 != 3:  # not last row
        if initial_state[x4+1][y4] == 0 and initial_state[x2+1][y2] == 0:  # get below
            get_double_neighbor(expanded_states, initial_state, x1, y1, x1+2, y1, x3, y3, x3+2, y3)
    if x1 != 0:  # not first row
        if initial_state[x1-1][y1] == 0 and initial_state[x3-1][y3] == 0:  # get up
            get_double_neighbor(expanded_states, initial_state, x4, y4, x4-2, y4, x2, y2, x2-2, y2)
    if y1 != 0:  # not first column
        if initial_state[x1][y1-1] == 0 and initial_state[x4][y4-1] == 0:  # get left
            get_double_neighbor(expanded_states, initial_state, x3, y3, x3, y3-2, x2, y2, x2, y2-2)
    if y2 != 3:  # not last column
        if initial_state[x3][y3+1] == 0 and initial_state[x2][y2+1] == 0:  # get right
            get_double_neighbor(expanded_states, initial_state, x1, y1, x1, y1+2, x4, y4, x4, y4+2)

    return expanded_states

def get_neighbor(expanded_states, initial_state, x, y, newX, newY):
    expanded_states.append(copy.deepcopy(initial_state))
    expanded_states[-1][x][y], expanded_states[-1][newX][newY] = expanded_states[-1][newX][newY], expanded_states[-1][x][y]

def get_double_neighbor(expanded_states, initial_state, x1, y1, newX1, newY1, x2, y2, newX2, newY2):
    expanded_states.append(copy.deepcopy(initial_state))
    expanded_states[-1][x1][y1], expanded_states[-1][newX1][newY1] = expanded_states[-1][newX1][newY1], expanded_states[-1][x1][y1]
    expanded_states[-1][x2][y2], expanded_states[-1][newX2][newY2] = expanded_states[-1][newX2][newY2], expanded_states[-1][x2][y2]

def uniform_cost_search(initial_state):
    """Finds the path taken by the uniform cost search algorithm
       Parameters
       ----------
       initial_state: 2-dimensional array representing initial block world config
       Returns
       -------
       path: (sequence of states to solve the block world) type - list of 2D arrays
    """
    path = []

    visited = []
    visitedNodes = []

    initial_node = Node(initial_state, [])
    queue = deque([initial_node])
    final = []

    while queue:
        node = queue.pop()
        if node.point not in visited:
            visited.append(node.point)
            visitedNodes.append(node)

            if goalAchieved(node.point):
                final = node
                break
            for neighbor in get_successors(node.point):
                if neighbor not in visited:
                    nd = Node(neighbor, node.point)
                    queue.appendleft(nd)

    path.append(final.point)
    for i in visitedNodes[::-1]:
        if i.point == final.parent:
            path.append(i.point)
            final = i

    return path[::-1]

def goalAchieved(current_state):
    if current_state[2][0] == 4 and current_state[3][0] == 4 and current_state[2][1] == 4 and current_state[3][1] == 4:
        return True
    else:
        return False


def a_star_heuristic(state):
    """Euclidean distance heuristic for a star algorithm
       Parameters
       ----------
       state: 2-dimensional array representing block world state
       Returns
       -------
       Euclidean distance (type- float) as defined in the assignment description
    """
    quad = []
    for i in range(len(state)):
        for j in  range(len(state)):
            if state[i][j] == 4:
                quad.append((i,j))
    return math.sqrt(math.pow(quad[2][0]-3,2)+math.pow(quad[2][1],2))


def a_star_search(initial_state):
    """Finds the path taken by the a star search algorithm
       Parameters
       ----------
       initial_state: 2-dimensional array representing initial block world config
       Returns
       -------
       path: (sequence of states to solve the block world) type-list of 2D arrays
    """
    path = []

    visited = []
    visitedNodes = []

    queue = PriorityQueue()
    queue.put((0, initial_state, []))
    final = []

    while queue:
        cost, point, parent = queue.get()

        if point not in visited:
            visited.append(point)
            visitedNodes.append(Node(point,parent))

            if goalAchieved(point):
                final = Node(point,parent)
                break
            for neighbor in get_successors(point):
                if neighbor not in visited:
                    queue.put((a_star_heuristic(neighbor) + cost, neighbor, point))

    path.append(final.point)
    for i in visitedNodes[::-1]:
        if i.point == final.parent:
            path.append(i.point)
            final = i

    return path[::-1]