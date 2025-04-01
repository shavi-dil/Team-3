from collections import deque
import functools
from Node import Node 
import PriorityQueue

def memoize(fn, slot = None, maxsize = 32):
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize = maxsize)
        def memoized_fn(*args):
            return fn(*args)
        
    return memoized_fn

def breadth_first_graph_search(problem):
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = deque([node])
    explored = set()
    
    while frontier():
        node = frontier.popleft()
        explored.add(node.state)

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)

    return None

def depth_first_graph_search(problem):
    frontier = [Node(problem.initial)] #Stack

    explored = set()
    while frontier:
        node = frontier.pop()

        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and child not in frontier)

    return None

def best_first_graph_search(problem, f, display = False):
    #Specify h(x) = f(x) for greedy best first search
    f = memoize(f, 'f')

    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()

    while frontier:
        node = frontier.pop()

        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        
        explored.add(node.state)

        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)

    return None

def astar_search(problem, h = None, display = False):
    h = memoize(h or problem.h, 'h')

    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

def depth_limited_search(problem, limit):
    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    return recursive_dls(Node.Node(problem.initial), problem, limit)

def iterative_deepening_search(problem):
    for depth in range(0, 1000):  # You can change max depth if needed
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result
    return None

def weighted_astar_search(problem, h=None, w=2.0, display=False):
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + w * h(n), display)
