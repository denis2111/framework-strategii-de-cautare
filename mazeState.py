from problemState import ProblemState, ProblemType
from utils.scoreFunction import compute_score


class MazeState(ProblemState):
    def __init__(self, n, m, start_position, current_position, end_position, maze, score_function_expr="0"):
        super().__init__()

        self.n = n
        self.m = m
        self.start_position = start_position
        self.end_position = end_position
        self.maze = maze
        self.current_position = current_position
        self.score_function_expr = score_function_expr

    def __is_valid_state(self, position):
        x, y = position
        if x < 0 or x >= self.n:
            return False
        if y < 0 or y >= self.m:
            return False
        if self.maze[x][y] == 1:
            return False
        return True

    def __eq__(self, other):
        if self.current_position == other.current_position:
            return True
        return False

    def is_final_state(self):
        return self.current_position == self.end_position

    def get_next_states(self):
        dx = [0, 0, -1, 1]
        dy = [-1, 1, 0, 0]

        next_states = []
        for next_state_delta in zip(dx, dy):
            next_x = self.current_position[0] + next_state_delta[0]
            next_y = self.current_position[1] + next_state_delta[1]

            if self.__is_valid_state((next_x, next_y)):
                next_states.append(MazeState(self.n,
                                             self.m,
                                             self.start_position,
                                             (next_x, next_y),
                                             self.end_position,
                                             self.maze, self.score_function_expr))

        return next_states

    def score_function(self):
        try:
            score = compute_score(self.score_function_expr, self)
            # print(self.score_function_expr)
            # print(score)
            if score == "wrong_function":
                raise Exception()
            else:
                return score
        except:
            return 0

    def get_reversed_problem(self):
        return MazeState(self.n,
                         self.m,
                         self.end_position,
                         self.end_position,
                         self.start_position,
                         self.maze)

    def get_problem_type(self):
        return ProblemType.MAZE
