from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue
from random import randint, randrange
from random import random as rnd
from typing import List

from problemState import ProblemState


class ProblemSolver:
    def __init__(self, problem: ProblemState):
        self.problem = problem

    # uninformed
    def random(self, steps=1000):
        """
        At each step this algorithm will choose a neighbour at random and will make the transition to it.

        :param steps: Number of steps the algorithm will do. If this number of steps is reached and a solution
        wasn't found, the algorithm will stop.
        :return: A dictionary with the following fields:
                "solution_found": True if a solution was found, else False.
                "visited_states": A list of visited states in the order of their visit.
                "solution": A path from the start state to a final state. If the field solution_found is False, this
                            field will be missing.
        """
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
            problem = next_state

        return {"solution_found": False,
                "visited_states": visited_states,
                }

    def BKT(self, problem=None, visited_states=None, solution=None):
        """
        At each step this algorithm will choose an unvisited neighbour and continue until it reach a final state or
        until there are no more unvisited neighbors and the algorithm will return until it can go on other path. It
        can visit the same state more then once but in different paths.

        :param problem: It is only for recursion, let is None.
        :param visited_states: It is only for recursion, let is None.
        :param solution: It is only for recursion, let is None.
        :return: A dictionary with the following fields:
                "solution_found": True if a solution was found, else False.
                "visited_states": A list of visited states in the order of their visit. If the algorithm returns from
                a state, it will appear for the second time in visited_states.
                "solution": A path from the start state to a final state. If the field solution_found is False, this
                            field will be missing.
        """
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
            if answer["solution_found"]:
                return answer
            visited_states.append(next_state)
            solution.pop()

        return {"solution_found": False,
                "visited_states": visited_states,
                }

    def DFS(self, problem=None, visited_states=None, solution=None):
        """
        At each step this algorithm will choose an unvisited neighbour and continue until it reach a final state or
        until there are no more unvisited neighbors and the algorithm will return until it can go on other unvisited
        neighbour. It will never visit the same state twice.

        :param problem: It is only for recursion, let is None.
        :param visited_states: It is only for recursion, let is None.
        :param solution: It is only for recursion, let is None.
        :return: A dictionary with the following fields:
                "solution_found": True if a solution was found, else False.
                "visited_states": A list of visited states in the order of their visit. If the algorithm returns from
                a state, it will appear for the second time in visited_states.
                "solution": A path from the start state to a final state. If the field solution_found is False, this
                            field will be missing.
        """
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
            if answer["solution_found"]:
                return answer
            visited_states.append(next_state)
            solution.pop()

        return {"solution_found": False,
                "visited_states": visited_states,
                }

    def bidirectional(self):
        """
        It is the same with BFS but it will start to visit states from the both start state and end state in
        the same time.

        :return: A dictionary with the following fields:
                "solution_found": True if a solution was found, else False.
                "visited_states": A list of visited states in the order of their visit.
                "solution": A path from the start state to a final state. If the field solution_found is False, this
                            field will be missing.
        :return:
        """
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
        """
        At each step this algorithm will visit a new state which is the closest unvisited state from the start.

        :return: A dictionary with the following fields:
                "solution_found": True if a solution was found, else False.
                "visited_states": A list of visited states in the order of their visit.
                "solution": A path from the start state to a final state. If the field solution_found is False, this
                            field will be missing.
        """
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
        """
        At each step this algorithm will visit a new state which is closer than current state to final state. If
        there is more than one such state it will choose one at random.
        To determine how close a state is to the final state, this algorithm will use the score_function from the
        problem_state.

        :return: A dictionary with the following fields:
                "solution_found": True if a solution was found, else False.
                "visited_states": A list of visited states in the order of their visit.
                "solution": A path from the start state to a final state. If the field solution_found is False, this
                            field will be missing.
        """
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

    @staticmethod
    def __choose_worse(next_states: List[ProblemState], current_score):
        worse_neighbours = []

        # Selectam vecinii cu distanta cea mai mica
        for state in next_states:
            if state.score_function() >= current_score:
                worse_neighbours.append(state)

        # Returnam unul dintre cei mai buni vecini random si distanta
        if not len(worse_neighbours):
            return None
        random_counter = randint(0, len(worse_neighbours) - 1)
        return worse_neighbours[random_counter]

    def simulated_annealing(self, steps_number=1000, cooling_function=None, start_temp=0.5):
        """
        This algorithm will choose a better neighbour like Hill climbing algorithm but it has a chance named temperature
        to choose a worse neighbour.

        :param steps_number: The number of steps after the algorithm will stop.
        :param cooling_function: The function for temperature cooling, it will be called in each setp. It must
        have one parameter temp and return the temperature after cooling.
        :param start_temp: The start temperature value. It must be in interval [0,1]
        :return:
        """
        if cooling_function is None:
            cooling_function = (lambda x: x * 0.98)
        problem = self.problem

        path = [problem]

        temp = start_temp
        while not problem.is_final_state() and steps_number > 0:
            next_states = problem.get_next_states()
            if not len(next_states):
                break

            if rnd() <= temp:
                next_state = ProblemSolver.__choose_worse(next_states, problem.score_function())
                if next_state:
                    problem = next_state
                    path.append(problem)
            else:
                next_state = ProblemSolver.__choice(next_states, problem.score_function())
                if next_state:
                    problem = next_state
                    path.append(problem)

            steps_number -= 1
            temp = cooling_function(temp)

        if problem.is_final_state():
            return {"solution_found": True,
                    "visited_states": path,
                    "solution": path,
                    }
        else:
            return {"solution_found": False,
                    "visited_states": path,
                    }

    def greedy(self):
        """
        At each step this algorithm will visit a new state which is closest to the final state among all neighbours.
        To determine how close a state is to the final state, this algorithm will use the score_function from the
        problem_state.

        :return: A dictionary with the following fields:
                "solution_found": True if a solution was found, else False.
                "visited_states": A list of visited states in the order of their visit.
                "solution": A path from the start state to a final state. If the field solution_found is False, this
                            field will be missing.
        """
        problem = self.problem

        possible_states = PriorityQueue()
        possible_states.put(ComparableItem(problem.score_function(), (problem, None)))
        visited_states = []

        while not possible_states.empty():

            # get the state with the best score from possible_states queue
            current_state, previous_state = possible_states.get().item
            if current_state in [vs[0] for vs in visited_states]:
                continue
            visited_states.append((current_state, previous_state))

            if current_state.is_final_state():
                return {"solution_found": True,
                        "visited_states": [vs[0] for vs in visited_states],
                        "solution": self.__get_bfs_solution([vs[0] for vs in visited_states],
                                                            [vs[1] for vs in visited_states],
                                                            len(visited_states) - 1),
                        }

            next_states = current_state.get_next_states()
            for next_state in next_states:
                possible_states.put(ComparableItem(next_state.score_function(), (next_state, len(visited_states) - 1)))

        return {"solution_found": False,
                "visited_states": [vs[0] for vs in visited_states],
                }

    def a_star(self):
        """
        At each step this algorithm will visit a new state which has the lowest value of: distance_from_start_state +
        problem_state.score_function().

        To determine how close a state is to the final state, this algorithm will use the score_function from the
        problem_state.

        :return: A dictionary with the following fields:
                "solution_found": True if a solution was found, else False.
                "visited_states": A list of visited states in the order of their visit.
                "solution": A path from the start state to a final state. If the field solution_found is False, this
                            field will be missing.
        """
        problem = self.problem

        possible_states = PriorityQueue()
        possible_states.put(ComparableItem(problem.score_function(), (problem, None, 0)))
        visited_states = []

        while not possible_states.empty():

            # get the state with the best score from possible_states queue
            current_state, previous_state, path_length = possible_states.get().item
            if current_state in [vs[0] for vs in visited_states]:
                continue
            visited_states.append((current_state, previous_state))

            if current_state.is_final_state():
                return {"solution_found": True,
                        "visited_states": [vs[0] for vs in visited_states],
                        "solution": self.__get_bfs_solution([vs[0] for vs in visited_states],
                                                            [vs[1] for vs in visited_states],
                                                            len(visited_states) - 1),
                        }

            next_states = current_state.get_next_states()
            for next_state in next_states:
                possible_states.put(ComparableItem(next_state.score_function() + path_length,
                                                   (next_state, len(visited_states) - 1, path_length + 1)))

        return {"solution_found": False,
                "visited_states": [vs[0] for vs in visited_states],
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


@dataclass(order=True)
class ComparableItem:
    priority: int
    item: Any=field(compare=False)