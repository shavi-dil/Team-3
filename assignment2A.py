import sys
from RouteFindingProblem import RouteFindingProblem
import Searches

def depthFirstSearch(problem):
    return Searches.depth_first_graph_search(problem)

def breadthFirstSearch(problem):
    return Searches.breadth_first_graph_search(problem)

def greedyBestFirstSearch(problem):
    return Searches.best_first_graph_search(problem, problem.h)

def aStarSearch(problem):
    return Searches.astar_search(problem)

def cus1(problem):
    return Searches.iterative_deepening_search(problem)

def cus2(problem):
    return Searches.weighted_astar_search(problem, w=2.0)

def format_output(file_name, method, goal_node):
    if goal_node is None:
        return f"{file_name} {method}\nNo path found"
    
    path = goal_node.solution()
    steps = len(goal_node.path()) - 1
    goal = goal_node.state
    cost = goal_node.path_cost 
    return f"{file_name} {method}\n{goal} {steps}\n{' -> '.join(map(str, path))}"

def main():
    if len(sys.argv) != 3:
        print("Usage: python assignment2A.py <input_file> <search_method>")
        return

    file_name = sys.argv[1]
    method = sys.argv[2].lower()

    problem = RouteFindingProblem(file_name)

    match method:
        case "dfs":
            result = depthFirstSearch(problem)
        case "bfs":
            result = breadthFirstSearch(problem)
        case "gbfs":
            result = greedyBestFirstSearch(problem)
        case "as":
            result = aStarSearch(problem)
        case "cus1":
            result = cus1(problem)
        case "cus2":
            result = cus2(problem)
        case _:
            print(f"Unknown method: {method}")
            return

    print(format_output(file_name, method, result))

if __name__ == "__main__":
    main()
