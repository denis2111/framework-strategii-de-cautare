from random import randint
from typing import List

from problemState import ProblemState


class ProblemSolver:
    def __init__(self, problem: ProblemState):
        self.problem = problem

# uninformed
    def BKT(self, problem=None, visited_states=None):
        if problem is None:
            problem = self.problem
            visited_states = [problem]

        if problem.is_final_state():
            return visited_states

        next_states = problem.get_next_states()

        for next_state in next_states:
            if next_state in visited_states:
                continue

            visited_states.append(next_state)
            solution = self.BKT(next_state, visited_states)
            if solution:
                return solution
            visited_states.pop()

        return None

# informed
    def hill_climbing(self):
        problem = self.problem

        best_global = problem.score_function()
        path = [problem]

        while not problem.is_final_state():
            next_states = problem.get_next_states()

            if len(next_states) == 0:
                return path

            next_state = ProblemSolver.__choice(next_states, problem.score_function())
            if not next_state:
                return path
            best_local = next_state.score_function()

            if best_local > best_global:
                return path
            else:
                best_global = best_local
                problem = next_state
                path.append(problem)

        return path

    @staticmethod
    def __choice(next_states: List[ProblemState], current_score):
        better_neighbours = []

        # Selectam vecinii cu distanta cea mai mica
        for state in next_states:
            if state.score_function() < current_score:
                better_neighbours.append(state)

        # Returnam unul dintre cei mai buni vecini random si distanta
        if not len(better_neighbours):
            return None
        random_counter = randint(0, len(better_neighbours) - 1)
        return better_neighbours[random_counter]

    def greedy(self):
        problem = self.problem

        best_global = problem.score_function()
        path = [problem]

        while not problem.is_final_state():
            next_states = problem.get_next_states()

            if len(next_states) == 0:
                return path

            next_state = ProblemSolver.__best_choice(next_states)
            best_local = next_state.score_function()

            if best_local > best_global:
                return path
            else:
                best_global = best_local
                problem = next_state
                path.append(problem)

        return path

    @staticmethod
    def __best_choice(next_states: List[ProblemState]):
        better_neighbours = []
        distance = next_states[0].score_function()
        best_distance = distance

        # Calculam distanta cea mai mica
        for state in next_states:
            distance = state.score_function()
            if distance < best_distance:
                best_distance = distance

        # Selectam vecinii cu distanta cea mai mica
        for state in next_states:
            if state.score_function() == best_distance:
                better_neighbours.append(state)

        # Returnam unul dintre cei mai buni vecini random si distanta
        random_counter = randint(0, len(better_neighbours) - 1)
        return better_neighbours[random_counter]