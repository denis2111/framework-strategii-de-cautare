from problemState import ProblemState


class MazeState(ProblemState):
    def __init__(self, n, m, start_position, current_position, end_position, maze):
        super().__init__()

        self.n = n
        self.m = m
        self.start_position = start_position
        self.end_position = end_position
        self.maze = maze
        self.current_position = current_position

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
                                             self.maze))

        return next_states

    def score_function(self):
      # manhatan distance
        x, y = self.current_position
        x2, y2 = self.end_position
        return abs(x - x2) + abs(y - y2)