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