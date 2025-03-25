import sys

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