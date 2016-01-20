# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False 

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False 

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True 

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True 

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True 

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False 

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph
import copy

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    path_queue = [[start]]
    if start == goal:
        return [start]
    while len(path_queue) != 0:
        first_path = path_queue[0]
        path_queue = path_queue[1:]
        end_node = first_path[-1]
        connected_nodes = graph.get_connected_nodes(end_node)
        for connect_node in connected_nodes:
            if connect_node in first_path:
                continue
            new_path = copy.deepcopy(first_path)
            new_path.append(connect_node)
            if connect_node == goal:
                return new_path
            path_queue.append(new_path)

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    path_queue = [[start]]
    if start == goal:
        return [start]
    while len(path_queue) != 0:
        first_path = path_queue[0]
        path_queue = path_queue[1:]
        end_node = first_path[-1]
        connected_nodes = graph.get_connected_nodes(end_node)
        for connect_node in connected_nodes:
            if connect_node in first_path:
                continue
            new_path = copy.deepcopy(first_path)
            new_path.append(connect_node)
            if connect_node == goal:
                return new_path
            path_queue = [new_path] + path_queue


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    path_queue = [[start]]
    if start == goal:
        return [start]
    while len(path_queue) != 0:
        first_path = path_queue[0]
        path_queue = path_queue[1:]
        end_node = first_path[-1]
        connected_nodes = graph.get_connected_nodes(end_node)
        smallest = float("inf")
        for connect_node in connected_nodes:
            if connect_node in first_path:
                continue
            new_path = copy.deepcopy(first_path)
            new_path.append(connect_node)
            if connect_node == goal:
                return new_path
            if graph.get_heuristic(connect_node, goal) < smallest:
                path_queue = [new_path] + path_queue
                smallest = graph.get_heuristic(connect_node, goal)
            else:
                path_queue = [path_queue[0]] + [new_path] + path_queue[1:]
    return []


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    path_queue = [[start], None]
    if start == goal:
        return [start]
    extended_path_same_level = []
    extended_path_heuristic_val = []
    while len(path_queue) != 0:
        first_path = path_queue[0]
        path_queue = path_queue[1:]
        if first_path == None:
            indexes = [i[0] for i in sorted(enumerate(extended_path_heuristic_val), key=lambda x:x[1])]
            for i in range(min(beam_width, len(indexes))):
                path_queue.append(extended_path_same_level[indexes[i]])
            if len(indexes) != 0:
                path_queue.append(None)
            extended_path_heuristic_val = []
            extended_path_same_level = []
            continue

        end_node = first_path[-1]
        if end_node == goal:
            return first_path
        connected_nodes = graph.get_connected_nodes(end_node)
        for connect_node in connected_nodes:
            if connect_node in first_path:
                continue
            new_path = copy.deepcopy(first_path)
            new_path.append(connect_node)
            extended_path_same_level.append(new_path)
            extended_path_heuristic_val.append(graph.get_heuristic(connect_node, goal))
    return []



## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    if len(node_names) == 1:
        return 0
    length = 0
    for i in range(len(node_names) - 1):
        length += graph.get_edge(node_names[i], node_names[i + 1]).length
    return length

def branch_and_bound(graph, start, goal):
    path_queue = [[start]]
    if start == goal:
        return [start]
    while len(path_queue) != 0:
        path_len = []
        for i in range(len(path_queue)):
            path_len.append(path_length(graph, path_queue[i]))
        indexes = [i[0] for i in sorted(enumerate(path_len), key = lambda x:x[1])]
        new_queue = []
        for i in indexes:
            new_queue.append(path_queue[indexes[i]])
        path_queue = new_queue
        first_path = path_queue[0]
        path_queue = path_queue[1:]
        end_node = first_path[-1]
        if end_node == goal:
            return first_path
        connected_nodes = graph.get_connected_nodes(end_node)
        for connect_node in connected_nodes:
            if connect_node in first_path:
                continue
            new_path = copy.deepcopy(first_path)
            new_path.append(connect_node)
            path_queue.append(new_path)
    return []

def a_star(graph, start, goal):
    path_queue = [[start]]
    if start == goal:
        return [start]
    extended_set = []
    while len(path_queue) != 0:
        path_len = []
        for i in range(len(path_queue)):
            path_len.append(path_length(graph, path_queue[i]) + graph.get_heuristic(path_queue[i][-1], goal))
        indexes = [i[0] for i in sorted(enumerate(path_len), key = lambda x:x[1])]
        new_queue = []
        for i in indexes:
            new_queue.append(path_queue[indexes[i]])
        path_queue = new_queue
        first_path = path_queue[0]
        path_queue = path_queue[1:]
        end_node = first_path[-1]
        if end_node == goal:
            return first_path
        if end_node in extended_set:
            continue
        extended_set.append(end_node)
        connected_nodes = graph.get_connected_nodes(end_node)
        for connect_node in connected_nodes:
            if connect_node in first_path:
                continue
            new_path = copy.deepcopy(first_path)
            new_path.append(connect_node)
            path_queue.append(new_path)
    return []

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for node in graph.nodes:
        shortest_path = branch_and_bound(graph, node, goal)
        shortest_path = path_length(graph, shortest_path)
        if graph.get_heuristic(node, goal) > shortest_path:
            return False
    return True

def is_consistent(graph, goal):
    for edge in graph.edges:
        if edge.length < abs(graph.get_heuristic(edge.node1, goal) - graph.get_heuristic(edge.node2, goal)):
            return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = ''
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
