import sys
import Searches

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