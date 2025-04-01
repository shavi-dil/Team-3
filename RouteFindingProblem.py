from problem import problem
import math

class RouteFindingProblem(problem):
    def __init__(self, file_path):
        self.nodes = {}       # node_id -> (x, y)
        self.edges = {}       # (from, to) -> cost
        self.graph = {}       # from -> list of (to, cost)

        self.initial = None
        self.goal = []

        self.parse_file(file_path)

    def parse_file(self, path):
        with open(path, 'r') as f:
            lines = f.read().splitlines()
        
        section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Nodes:"):
                section = "nodes"
            elif line.startswith("Edges:"):
                section = "edges"
            elif line.startswith("Origin:"):
                section = "origin"
            elif line.startswith("Destinations:"):
                section = "destinations"
            elif section == "nodes":
                node_id, coord = line.split(":")
                x, y = eval(coord.strip())
                self.nodes[int(node_id)] = (x, y)
            elif section == "edges":
                edge_str, cost = line.split(":")
                from_node, to_node = eval(edge_str.strip())
                self.edges[(from_node, to_node)] = int(cost)
                if from_node not in self.graph:
                    self.graph[from_node] = []
                self.graph[from_node].append((to_node, int(cost)))
            elif section == "origin":
                self.initial = int(line)
            elif section == "destinations":
                self.goal = [int(g.strip()) for g in line.split(";")]

    def actions(self, state):
        return [to for (to, _) in self.graph.get(state, [])]

    def result(self, state, action):
        return action

    def goal_test(self, state):
        return state in self.goal

    def path_cost(self, c, state1, action, state2):
        return c + self.get_cost(state1, state2)

    def get_cost(self, from_node, to_node):
        return self.edges.get((from_node, to_node), float('inf'))

    def h(self, node):
        # Use straight-line (Euclidean) distance to the closest goal
        x1, y1 = self.nodes[node.state]
        return min(math.hypot(x1 - self.nodes[g][0], y1 - self.nodes[g][1]) for g in self.goal)
