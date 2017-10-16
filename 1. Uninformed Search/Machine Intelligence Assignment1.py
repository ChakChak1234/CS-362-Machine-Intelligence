import copy

def expand(initial_state):
    """Successor function for the 8-puzzle variant
       Parameters
       ----------
       initial_state: 2-dimensional array representing initial 8-puzzle config
       Returns
       -------
       expanded_states: type- list of 2D arrrays
       """
    expanded_states = []
    for i in range(len(initial_state)):
        for j in range(len(initial_state)):
            if initial_state[i][j] == 0:
                if i % 2 == 1 or j % 2 == 1:  # non corner places with three neighbors
                    expanded_states.append(copy.deepcopy(initial_state))  # change it with middle (solution)
                    expanded_states[-1][i][j], expanded_states[-1][1][1] = expanded_states[-1][1][1], expanded_states[-1][i][j]
                    if i != 1:
                        expanded_states.append(copy.deepcopy(initial_state))
                        expanded_states[-1][i][j], expanded_states[-1][i][0] = expanded_states[-1][i][0], expanded_states[-1][i][j]

                        expanded_states.append(copy.deepcopy(initial_state))
                        expanded_states[-1][i][j], expanded_states[-1][i][2] = expanded_states[-1][i][2], expanded_states[-1][i][j]
                    elif j != 1:
                        expanded_states.append(copy.deepcopy(initial_state))
                        expanded_states[-1][i][j], expanded_states[-1][0][j] = expanded_states[-1][0][j], expanded_states[-1][i][j]

                        expanded_states.append(copy.deepcopy(initial_state))
                        expanded_states[-1][i][j], expanded_states[-1][2][j] = expanded_states[-1][2][j], expanded_states[-1][i][j]
                else:  # corners with only two neighbors
                    expanded_states.append(copy.deepcopy(initial_state))
                    expanded_states[-1][i][j], expanded_states[-1][i][1] = expanded_states[-1][i][1], expanded_states[-1][i][j]  # horizontal change

                    expanded_states.append(copy.deepcopy(initial_state))
                    expanded_states[-1][i][j], expanded_states[-1][1][j] = expanded_states[-1][1][j], expanded_states[-1][i][j]  # vertical change
                return expanded_states

def graph_search(initial_state):
    """Defines the path taken by the breadth-first search algorithm
       Parameters
       ----------
       initial_state: 2-dimensional array representing initial 8-puzzle config
       Returns
       -------
       path: (sequence of states to solve the 8-puzzle variant)type-list of 2D arrays
       """
    path = [initial_state]
    current_node = copy.deepcopy(initial_state)
    while True:
        count = len(path)
        result = expand(current_node)
        for i in result:
            if i[1][1] == 0:
                path.append(i)
                break
        if len(path) > count:
            break
        else:
            current_node = result[-1]
            path.append(result[-1])
    return path