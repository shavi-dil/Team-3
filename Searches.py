from collections import deque
import functools
import Node
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