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
    return f"{file_name}\n{method}\n{goal} {steps}\n{' -> '.join(map(str, path))}"

def main():
    if len(sys.argv) != 3:
        print("Usage: python assignment2A.py <input_file> <search_method>")
        return

    file_name = sys.argv[1]
    method = sys.argv[2].lower()

    problem = RouteFindingProblem(file_name)

    match method:
        case "dfs":
            longMethod = "Depth First Search"
            result = depthFirstSearch(problem)
        case "bfs":
            longMethod = "Breadth First Search"
            result = breadthFirstSearch(problem)
        case "gbfs":
            longMethod = "Greedy Best First Search"
            result = greedyBestFirstSearch(problem)
        case "as":
            longMethod = "A* Search"
            result = aStarSearch(problem)
        case "cus1":
            longMethod = "Iterative Deepening Search"
            result = cus1(problem)
        case "cus2":
            longMethod = "Weighted A* Search"
            result = cus2(problem)
        case _:
            print(f"Unknown method: {method}")
            return

    print(format_output(file_name, longMethod, result))

if __name__ == "__main__":
    main()
