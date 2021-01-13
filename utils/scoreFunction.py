from typing import List
from mpmath import sin, cos, tan, cot, sqrt
from copy import deepcopy
from problemState import ProblemState, ProblemType


def sqrt_ord(value: float, ord: float):
    return value ** (1 / ord)


def list_index(container: List[float], value):
    return container.index(value)


def list_prod(container: List[float]):
    prod = 1
    for i in container:
        prod *= i
    return prod


def matrix_min(container: List[List[float]]):
    minimum = container[0][0]
    for column in container:
        if minimum > min(column):
            minimum = min(column)
    return minimum


def matrix_max(container: List[List[float]]):
    maximum = container[0][0]
    for column in container:
        if maximum < max(column):
            maximum = max(column)
    return maximum


def matrix_sum(container: List[List[float]]):
    items_sum = 0
    for column in container:
        items_sum += sum(column)
    return items_sum


def matrix_prod(container: List[List[float]]):
    items_prod = 1
    for column in container:
        items_prod *= list_prod(column)
    return items_prod


def matrix_column_index(container: List[List[float]], value):
    for column in range(len(container)):
        for line in range(len(container[0])):
            if value == container[line][column]:
                return column


def matrix_line_index(container: List[List[float]], value):
    for column in range(len(container)):
        for line in range(len(container[0])):
            if value == container[line][column]:
                return line


default_valid_functions = {
    '__builtins__': None,
    "sqrt": sqrt,
    "sqrt_ord": sqrt_ord,
    "sin": sin,
    "cos": cos,
    "tg": tan,
    "ctg": cot,

    "abs": abs,
    "min": min,
    "max": max,
}


def matrix_compute_score(expression: str, problem):
    number_of_lines = problem.n
    number_of_columns = problem.m
    current_line, current_column = problem.current_position
    final_line, final_column = problem.end_position
    start_line, start_column = problem.start_position
    # print(current_line, current_column)
    # print(final_line, final_column)

    container = deepcopy(problem.maze)

    custom_valid_functions = {
        "line_min": min,
        "line_max": max,
        "line_sum": sum,
        "line_prod": list_prod,

        "matrix_min": matrix_min,
        "matrix_max": matrix_max,
        "matrix_sum": matrix_sum,
        "matrix_prod": matrix_prod,
        "matrix_column_index": matrix_column_index,
        "matrix_line_index": matrix_line_index,

        "number_of_lines": number_of_lines,
        "number_of_columns": number_of_columns,
        "current_line": current_line,
        "current_column": current_column,
        "final_line": final_line,
        "final_column": final_column,
        "start_line": start_line,
        "start_column": start_column,
        "container": container,
    }
    all_valid_functions = default_valid_functions.copy()
    all_valid_functions.update(custom_valid_functions)

    try:
        expression_value = eval(expression, all_valid_functions)
        if expression_value is None or "=" in expression:
            raise Exception
        return expression_value
    except:
        return "wrong function"


def list_compute_score(expression: str, problem):
    number_of_poles = problem.nr_poles
    number_of_pieces = problem.nr_pieces
    container = deepcopy(problem.representation[1:])

    custom_valid_functions = {
        "list_min": min,
        "list_max": max,
        "list_sum": sum,
        "list_prod": list_prod,

        "number_of_poles": number_of_poles,
        "number_of_pieces": number_of_pieces,
        "container": container,
    }
    all_valid_functions = default_valid_functions.copy()
    all_valid_functions.update(custom_valid_functions)

    try:
        expression_value = eval(expression, all_valid_functions)
        if expression_value is None or "=" in expression:
            raise Exception
        return expression_value
    except:
        return "wrong function"


def compute_score(expression, problem: ProblemState):
    if problem.get_problem_type() == ProblemType.MAZE:
        return matrix_compute_score(expression, problem)
    elif problem.get_problem_type() == ProblemType.HANOI:
        return list_compute_score(expression, problem)
    else:
        return None


# euclidian distance
# expression = "sqrt((current_line - final_line)**2 + (current_column - final_column)**2)"
# manhaten distance
# expression = "abs(current_line - final_line) + abs(current_column - final_column)"
# chebyshev distance
# expression = "max(abs(current_line - final_line), abs(current_column - final_column))"
