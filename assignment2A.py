import sys
from collections import deque
import functools
import heapq

def depthFirstSearch():
    return("Depth first search")

def breadthFirstSearch():
    return("Breadth first search")

def greedyBestFirstSearch():
    return("Greedy!")

def aStarSearch():
    return("A star!")

def main():
    file = open(sys.argv[1], "r")
    nodes = file.read()
    
    match sys.argv[2].lower():
        case "dfs":
            print(depthFirstSearch())
        case "bfs":
            print(breadthFirstSearch())
        case "gbfs":
            print(greedyBestFirstSearch())
        case "as":
            print(aStarSearch())


main()

class problem():
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError
    
    def result(self, state, action):
        raise NotImplementedError
    
    def goal_test(self, state):
        if isinstance(self.goal, list):
            return any(x is state for x in self.goal)
        else:
            return state == self.goal
        
    def path_cost(self, c, state1, action, state2):
        return c + 1
    
    def value(self, state):
        raise NotImplementedError
    
class Node:
    def __init__(self, state, parent = None, action = None, path_cost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    def __repr__(self):
        return "<Node {}>".format(self.state)
    
    def __lt__(self, node):
        return self.state < node.state
    
    def expand(self, problem):
        return [self.child_node(problem, action) for action in problem.actions(self.state)]
    
    def child_node(self, problem, action):
        next_state = problem.result(self.sate, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node
    
    def solution(self):
        return [node.action for node in self.path()[1:]]
    
    def path(self):
        node, path_back = self, []

        while node:
            path_back.append(node)
            node = node.parent
        
        return list(reversed(path_back))
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state
    
    def __hash__(self):
        return hash(self.state)
    
class SimpleProblemSolvingAgentProgram:
    def __init__(self, initial_state = None):
        self.state = initial_state
        self.seq = []

    def __call__(self, percept):
        self.state = self.update_state(self.state, percept)
        if not self.seq:
            goal = self.formulate_goal(self.state)
            problem = self.formulate_problem(self.state, goal)
            self.swq = self.search(problem)
            if not self.seq:
                return None
            
        return self.seq.pop(0)

    def update_state(self, state, percept):
        raise NotImplementedError
        
    def formulate_goal(self, state):
        raise NotImplementedError
        
    def formulate_problem(self, state, goal):
        raise NotImplementedError
    
class PriorityQueue:
    def __init__(self, order='min', f=lambda x: x):
        self.heap = []
        if order == 'min':
            self.f = f
        elif order == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
        else:
            raise ValueError("Order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)
    
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