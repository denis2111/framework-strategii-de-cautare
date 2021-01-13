from random import randint
from typing import List

from problemState import ProblemState


class ProblemSolver:
    def __init__(self, problem: ProblemState):
        self.problem = problem

    # uninformed
    def random(self, steps=1000):
        problem = self.problem
        visited_states = [problem]

        for i in range(steps):
            if problem.is_final_state():
                return {"solution_found": True,
                        "visited_states": visited_states,
                        "solution": visited_states,
                        }

            next_states = problem.get_next_states()
            next_state = next_states[randint(0, len(next_states) - 1)]
            visited_states.append(next_state)

        return {"solution_found": False,
                "visited_states": visited_states,
                }

    def BKT(self, problem=None, visited_states=None, solution=None):
        if problem is None:
            problem = self.problem
            visited_states = [problem]
            solution = [problem]

        if problem.is_final_state():
            return {"solution_found": True,
                    "visited_states": visited_states,
                    "solution": solution,
                    }

        next_states = problem.get_next_states()

        for next_state in next_states:
            if next_state in visited_states:
                continue

            visited_states.append(next_state)
            solution.append(next_state)
            answer = self.BKT(next_state, visited_states,solution)
            if answer:
                return answer
            visited_states.append(next_state)
            solution.pop()

        return None

    def DFS(self, problem=None, visited_states=None, solution=None):
        if problem is None:
            problem = self.problem
            visited_states = [problem]
            solution = [problem]

        if problem.is_final_state():
            return {"solution_found": True,
                    "visited_states": visited_states,
                    "solution": solution,
                    }

        next_states = problem.get_next_states()

        for next_state in next_states:
            if next_state in visited_states:
                continue

            visited_states.append(next_state)
            solution.append(next_state)
            answer = self.DFS(next_state, visited_states, solution)
            if answer:
                return answer
            visited_states.append(next_state)
            solution.pop()

        return None

    def bidirectional(self):
        problem = self.problem
        visited_states = [problem]
        states_queue = [problem]
        previous_states = [None]

        reversed_problem = problem.get_reversed_problem()
        reversed_visited_states = [reversed_problem]
        reversed_states_queue = [reversed_problem]
        steps_order = [problem, reversed_problem]
        reversed_previous_states = [None]

        while not problem in reversed_visited_states:
            next_states = problem.get_next_states()
            for next_state in next_states:
                if next_state in visited_states:
                    continue

                visited_states.append(next_state)
                previous_states.append(visited_states.index(problem))
                states_queue.append(next_state)
                steps_order.append(next_state)

                if next_state in reversed_visited_states:
                    return {"solution_found": True,
                            "visited_states": steps_order,
                            "solution": self.__get_bfs_solution(visited_states, previous_states , len(visited_states) - 1) +
                                        list(reversed(self.__get_bfs_solution(reversed_visited_states, reversed_previous_states,
                                                                reversed_visited_states.index(visited_states[-1]))[:-1]))
                            }

            if not states_queue:
                return {"solution_found": False,
                        "visited_states": steps_order,
                        }
            problem = states_queue.pop(0)

            if reversed_states_queue:
                reversed_problem = reversed_states_queue.pop(0)
                next_states = reversed_problem.get_next_states()

                for next_state in next_states:
                    if next_state in reversed_visited_states:
                        continue

                    if next_state in visited_states:
                        return steps_order

                    reversed_visited_states.append(next_state)
                    reversed_previous_states.append(reversed_visited_states.index(reversed_problem))
                    reversed_states_queue.append(next_state)
                    steps_order.append(next_state)

                    if next_state in visited_states:
                        return {"solution_found": True,
                                "visited_states": steps_order,
                                "solution": self.__get_bfs_solution(visited_states, previous_states,
                                                                    visited_states.index(reversed_visited_states[-1])) +
                                            list(reversed(self.__get_bfs_solution(reversed_visited_states,
                                                                                  reversed_previous_states,
                                                                                  len(reversed_visited_states) - 1)[:-1]))
                                }

        return {"solution_found": False,
                "visited_states": steps_order,
                }

    def BFS(self):
        problem = self.problem
        visited_states = [problem]
        previous_states = [None]
        states_queue = [problem]

        while not problem.is_final_state():
            next_states = problem.get_next_states()
            for state in next_states:
                if state in visited_states:
                    continue

                visited_states.append(state)
                previous_states.append(visited_states.index(problem))
                states_queue.append(state)

                if state.is_final_state():
                    return {"solution_found": True,
                            "visited_states": visited_states,
                            "solution": self.__get_bfs_solution(visited_states, previous_states, len(visited_states) - 1),
                            }

            if not states_queue:
                return {"solution_found": True,
                        "visited_states": visited_states,
                        }
            problem = states_queue.pop(0)

        return {"solution_found": True,
                "visited_states": visited_states,
                "solution": self.__get_bfs_solution(visited_states, previous_states, len(visited_states) - 1),
                }

    def __get_bfs_solution(self, visited_states, previous_states, start):
        current_pos = start
        solution = []
        while current_pos:
            solution.append(visited_states[current_pos])
            current_pos = previous_states[current_pos]
        solution.reverse()
        return solution

    # informed
    def hill_climbing(self):
        problem = self.problem

        best_global = problem.score_function()
        path = [problem]

        while not problem.is_final_state():
            next_states = problem.get_next_states()

            if len(next_states) == 0:
                return {"solution_found": False,
                        "visited_states": path,
                        }

            next_state = ProblemSolver.__choice(next_states, problem.score_function())
            if not next_state:
                return {"solution_found": False,
                        "visited_states": path,
                        }
            best_local = next_state.score_function()

            if best_local > best_global:
                return {"solution_found": False,
                        "visited_states": path,
                        }
            else:
                best_global = best_local
                problem = next_state
                path.append(problem)

        return {"solution_found": True,
                "visited_states": path,
                "solution": path,
                }

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
                return {"solution_found": False,
                        "visited_states": path,
                        }

            next_state = ProblemSolver.__best_choice(next_states)
            best_local = next_state.score_function()

            if best_local > best_global:
                return {"solution_found": False,
                        "visited_states": path,
                        }
            else:
                best_global = best_local
                problem = next_state
                path.append(problem)

        return {"solution_found": True,
                "visited_states": path,
                "solution": path,
                }

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
