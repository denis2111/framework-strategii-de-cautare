from random import randint
from typing import List

from problemState import ProblemState


class ProblemSolver:
    def __init__(self, problem: ProblemState):
        self.problem = problem

# uninformed
    def random(self, problem=None, visited_states=None):
        if problem is None:
            problem = self.problem
            visited_states = [problem]
        print(problem.current_position)

        if problem.is_final_state():
            return visited_states

        next_states = problem.get_next_states()
        next_state = next_states[randint(0, len(next_states) - 1)]
        visited_states.append(next_state)
        solution = self.random(next_state, visited_states)
        if solution:
            return solution

        return None

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

    def DFS(self, problem=None, visited_states=None):
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
            solution = self.DFS(next_state, visited_states)
            if solution:
                return solution

        return None

    def bidirectional(self):
        problem = self.problem
        reversed_problem = problem.get_reversed_problem()
        visited_states = [problem]
        states_queue = [problem]
        reversed_visited_states = [reversed_problem]
        reversed_states_queue = [reversed_problem]

        while not problem in reversed_visited_states:
            next_states = problem.get_next_states()
            for state in next_states:
                if state in visited_states:
                    continue

                visited_states.append(state)
                states_queue.append(state)

            if not states_queue:
                return visited_states
            problem = states_queue.pop(0)

            if reversed_states_queue:
                next_states = reversed_states_queue.pop().get_next_states()

                for state in next_states:
                    if state in reversed_visited_states:
                        continue

                    if state in visited_states:
                        return visited_states + reversed_visited_states

                    reversed_visited_states.append(state)
                    reversed_states_queue.append(state)

        return visited_states + reversed_visited_states

    def BFS(self):
        problem = self.problem
        visited_states = [problem]
        states_queue = [problem]

        while not problem.is_final_state():
            next_states = problem.get_next_states()
            for state in next_states:
                if state in visited_states:
                    continue

                visited_states.append(state)
                states_queue.append(state)

            if not states_queue:
                return visited_states
            problem = states_queue.pop(0)

        return visited_states

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