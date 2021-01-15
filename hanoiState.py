from problemState import ProblemState
from copy import deepcopy


class HanoiState(ProblemState):
    def __init__(self, nr_towers, nr_pieces, pieces):
        """
        :param nr_towers: number of towers
        :param nr_pieces: number of pieces
        :param pieces: a list of each piece's pole ordered in inverse order of piece size.
                e.g. : pieces[k]= i means the piece of size m-k+1 is on the tower i
                (the biggest piece is first, the smallest is the last)
        """
        super().__init__()
        assert (len(pieces) == nr_pieces)
        self.nr_poles = nr_towers
        self.nr_pieces = nr_pieces
        self.representation = [nr_towers] + pieces

    def is_final_state(self):
        biggest_piece_pole = self.representation[1]
        for piece_pole in self.representation[1:]:
            if piece_pole != biggest_piece_pole:
                return False
        return True

    def get_tower_of_piece(self, piece_size):
        return self.representation[self.nr_pieces - piece_size + 1]

    def get_tower_tops(self):
        """

        :return: result[x] = y means that the piece y is on top of tower x
                result[x] = -1 means that pole x is empty
        """
        result = {}
        for i in range(1, self.nr_poles + 1):
            result[i] = -1
        for piece_size in range(1, self.nr_pieces + 1):
            piece_tower = self.get_tower_of_piece(piece_size)
            if result[piece_tower] == -1:
                result[piece_tower] = piece_size
        return result

    def __eq__(self, other):
        for i in range(len(self.representation)):
            if self.representation[i] != other.representation[i]:
                return False
        return True

    def get_next_states(self):
        tower_tops = self.get_tower_tops()
        tops = list(tower_tops.values())
        next_states = []
        possible_moves = {}
        for piece in tops:
            if piece != -1:
                possible_moves[piece] = [tower for tower in tower_tops if
                                         tower_tops[tower] > piece or tower_tops[tower] == -1]
        for piece_to_be_moved, new_tower_choices in possible_moves.items():
            for new_tower in new_tower_choices:
                new_representation = deepcopy(self.representation)
                new_representation[self.nr_pieces - piece_to_be_moved + 1] = new_tower
                next_states.append(HanoiState(self.nr_poles, self.nr_pieces, new_representation[1:]))
        # print(next_states[0].representation)
        return next_states

    def tower_pieces(self):
        result = {}
        for tower_index in range(1, self.nr_poles + 1):
            result[tower_index] = []
        for piece_size in range(self.nr_pieces, 0, -1):
            tower_of_piece = self.get_tower_of_piece(piece_size)
            result[tower_of_piece].append(piece_size)
        return result


def my_func():
    print(type(range(5)))


if __name__ == '__main__':
    from problemSolver import ProblemSolver

    state = HanoiState(3, 6, [3, 3, 3, 2, 2, 1])
    print(getattr(state, "tower_pieces")())
    my_func()
    # print(state.tower_pieces())
    # state = HanoiState(3, 6, [1, 1, 1, 1, 2, 3])
    # print(state.is_final_state())
    # ps = ProblemSolver(state)
    # solution = ps.BKT()
    # solution = ps.DFS()
    # if solution:
    #     print("Am gasit ceva")
    # next_transitions = state.get_next_states()
    # for new_state in next_states:
    #     print(new_state.representation)