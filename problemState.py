from enum import Enum


class ProblemType(Enum):
    MAZE = 1
    HANOI = 2


class ProblemState:
    def __init__(self):
        pass

    def get_next_states(self):
        pass

    def is_final_state(self):
        pass

    def score_function(self):
        pass

    def get_reversed_problem(self):
        pass

    def get_problem_type(self):
        pass
