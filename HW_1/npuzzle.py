"""
COMS W4701 Artificial Intelligence - Programming Homework 1

In this assignment you will implement and compare different search strategies
for solving the n-Puzzle, which is a generalization of the 8 and 15 puzzle to
squares of arbitrary size (we will only test it with 8-puzzles for now).
See Courseworks for detailed instructions.

@author: Anthony Saieva (Narin) an2804
"""

import time

def state_to_string(state):
    row_strings = [" ".join([str(cell) for cell in row]) for row in state]
    return "\n".join(row_strings)


def swap_cells(state, i1, j1, i2, j2):
    """
    Returns a new state with the cells (i1,j1) and (i2,j2) swapped.
    """
    value1 = state[i1][j1]
    value2 = state[i2][j2]

    new_state = []
    for row in range(len(state)):
        new_row = []
        for column in range(len(state[row])):
            if row == i1 and column == j1:
                new_row.append(value2)
            elif row == i2 and column == j2:
                new_row.append(value1)
            else:
                new_row.append(state[row][column])
        new_state.append(tuple(new_row))
    return tuple(new_state)

def get_successors(state):
    """
    This function returns a list of possible successor states resulting
    from applicable actions.
    The result should be a list containing (Action, state) tuples.
    For example [("Up", ((1, 4, 2),(0, 5, 8),(3, 6, 7))),
                 ("Left",((4, 0, 2),(1, 5, 8),(3, 6, 7)))]
    """

    holeX = -1
    holeY = -1
    ACTIONS = ["Left", "Right","Up", "Down"]
    found = False
    for x in range(0,3):
        for y in range(0,3):
            if state[x][y] == 0:
                found = True
                holeX = x
                holeY = y
                break
        if found:
            break
    assert(holeX != -1)
    assert(holeY != -1)
    child_states = []

    # YOUR CODE HERE . Hint: Find the "hole" first, then generate each possible
    # successor state by calling the swap_cells method.
    # Exclude actions that are not applicable.

    if(holeY < 2):
        child_states.append((ACTIONS[0], swap_cells(state, holeX, holeY, holeX, holeY+1)))
    if(holeY > 0):
        child_states.append((ACTIONS[1], swap_cells(state, holeX, holeY, holeX, holeY-1)))
    if(holeX < 2):
        child_states.append((ACTIONS[2], swap_cells(state, holeX, holeY, holeX+1, holeY)))
    if(holeX > 0):
        child_states.append((ACTIONS[3], swap_cells(state, holeX, holeY, holeX-1, holeY)))


    return child_states


def goal_test(state):
    """
    Returns True if the state is a goal state, False otherwise.
    """

    goal_state = ((0,1,2),(3,4,5),(6,7,8))
    if goal_state == state:
        return True
    return False

def get_solution(mapping, state):
    """
    returns a list of actions ["RIGHT", "UP", ...]
    that are the solution based on the given mapping
    """
    actions = []
    search_state = state
    while(mapping[search_state] != 'initial_state'):
        actions.append(mapping[search_state][0])
        search_state = mapping[search_state][1]
    actions.reverse()
    return actions

def bfs(state):
    """
    Breadth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a queue in BFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    closed_list = []
    backtrack = {}

    #YOUR CODE HERE
    queue = []
    if len(queue) == 0:
        backtrack[state] = "initial_state"
        queue.append(state)

    while(len(queue) != 0):
        parent_state = queue.pop(0)

        if goal_test(parent_state):
            # need to return stuff here
            print("You found the goal")
            solution = get_solution(backtrack, parent_state)
            states_expanded = len(closed)
            # add one for the goal state that we found
            states_expanded += 1
            return solution, states_expanded, max_fringe

        successors = get_successors(parent_state)
        closed.add(parent_state)

        for node in successors:
            action = node[0]
            child_state = node[1]

            # Don't re add already closed nodes to the tree
            if child_state in closed:
                continue

            # update the mapping structure
            backtrack[child_state] = (action, parent_state)

            queue.append(child_state)
            if(len(queue) > max_fringe):
                max_fringe = len(queue)

    #  return solution, states_expanded, max_fringe
    return None, states_expanded, max_fringe # No solution found


def dfs(state):
    """
    Depth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a stack in DFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}
    #YOUR CODE HERE

    queue = []
    if len(queue) == 0:
        parents[state] = "initial_state"
        queue.append(state)

    while(len(queue) != 0):
        parent_state = queue.pop()

        if goal_test(parent_state):
            # need to return stuff here
            print("You found the goal")
            solution = get_solution(parents, parent_state)
            states_expanded = len(closed)
            # add one for the goal state that we found
            states_expanded += 1
            return solution, states_expanded, max_fringe

        successors = get_successors(parent_state)

        closed.add(parent_state)

        for node in successors:
            action = node[0]
            child_state = node[1]

            # Don't re add already closed nodes to the tree
            if child_state in closed:
                continue

            # update the mapping structure
            parents[child_state] = (action, parent_state)

            queue.append(child_state)
            if(len(queue) > max_fringe):
                max_fringe = len(queue)

    #  return solution, states_expanded, max_fringe
    return None, states_expanded, max_fringe # No solution found


def misplaced_heuristic(state):
    """
    Returns the number of misplaced tiles.
    """

    #YOUR CODE HERE
    count = 0
    goal_state = ((0,1,2),(3,4,5),(6,7,8))
    for x in range(0,3):
        for y in range(0,3):
            if state[x][y] != goal_state[x][y]:
                count += 1
    return count


def manhattan_heuristic(state):
    """
    For each misplaced tile, compute the Manhattan distance between the current
    position and the goal position. Then return the sum of all distances.
    """
    goal_placings = {
                     0:(0,0),
                     1:(0,1),
                     2:(0,2),
                     3:(1,0),
                     4:(1,1),
                     5:(1,2),
                     6:(2,0),
                     7:(2,1),
                     8:(2,2)
                     }
    total = 0
    for x in range(0,3):
        for y in range(0,3):
            num = state[x][y]
            diffX = abs(goal_placings[num][0]-x)
            diffY = abs(goal_placings[num][1]-y)
            total += diffX
            total += diffY

    return total


def best_first(state, heuristic):
    """
    Best first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    # You may want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}

    #YOUR CODE HERE
    if not fringe:
        parents[state] = "initial_state"
        pair = (heuristic(state), state)
        heappush(fringe, pair)

    while fringe:
        parent_pair = heappop(fringe)
        parent_state = parent_pair[1]

        if goal_test(parent_state):
            solved = get_solution(parents, parent_state)
            states_expanded = len(closed)
            # add one for goal state
            states_expanded += 1
            return solved, states_expanded, max_fringe

        successors = get_successors(parent_state)
        closed.add(parent_state)

        for node in successors:
            action = node[0]
            child_state = node[1]

            pair = (heuristic(child_state), child_state)

            # Don't re add already closed nodes to the tree
            if child_state in closed:
                continue

            parents[child_state] = (action, parent_state)

            heappush(fringe, pair)

            if len(fringe) > max_fringe:
                max_fringe = len(fringe)

    return None, states_expanded, max_fringe # No solution found


def astar(state, heuristic):
    """
    A-star search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    # You may want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}
    costs = {}

    #YOUR CODE HERE
    if not fringe:
        parents[state] = "initial_state"
        costs[state] = 0
        pair = (heuristic(state), state)
        heappush(fringe, pair)

    while fringe:
        parent_pair = heappop(fringe)
        parent_state = parent_pair[1]

        if goal_test(parent_state):
            solved = get_solution(parents, parent_state)
            states_expanded = len(closed)
            # add one for goal state
            states_expanded += 1
            return solved, states_expanded, max_fringe

        successors = get_successors(parent_state)
        closed.add(parent_state)

        for node in successors:
            action = node[0]
            child_state = node[1]

            # Don't re add already closed nodes to the tree
            if child_state in closed:
                continue

            cost = costs[parent_state] + 1
            pair = (cost + heuristic(child_state),
                    child_state)


            costs[child_state] = cost
            parents[child_state] = (action, parent_state)

            heappush(fringe, pair)

            if len(fringe) > max_fringe:
                max_fringe = len(fringe)


    return None, states_expanded, max_fringe # No solution found


def print_result(solution, states_expanded, max_fringe):
    """
    Helper function to format test output.
    """
    if solution is None:
        print("No solution found.")
    else:
        print("Solution has {} actions.".format(len(solution)))
    print("Total states expanded: {}.".format(states_expanded))
    print("Max fringe size: {}.".format(max_fringe))



if __name__ == "__main__":

    #Easy test case
    # test_state = ((1, 4, 2),
    #               (0, 5, 8),
    #               (3, 6, 7))

    # More difficult test case
    test_state = ((7, 2, 4),
                 (5, 0, 6),
                 (8, 3, 1))

    print(state_to_string(test_state))
    print()

    print("====BFS====")
    start = time.time()
    solution, states_expanded, max_fringe = bfs(test_state) #
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end-start))

    # print()
    print("====DFS====")
    start = time.time()
    solution, states_expanded, max_fringe = dfs(test_state)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====Greedy Best-First (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = best_first(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Total Manhattan Distance Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, manhattan_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))
