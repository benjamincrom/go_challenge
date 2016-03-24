'''
go.py --
'''
from copy import deepcopy

def char_range(c1, c2):
    for c in xrange(ord(c1), ord(c2)):
        yield chr(c)


class Move:
    def __init__(self, move_str):
        letter = move_str[0].lower()
        number = int(move_str[1:])
        self.location = (letter, number)

    def __repr__(self):
        return "Move('{}{}')".format(self.location[0], self.location[1])


class Board:
    def __init__(self):
        self.board_array = [[0 for _ in range(19)] for _ in range(19)]
        self.black_to_move = True
        self.all_locations = [
            (c, i) for c in char_range('a', 't') for i in range(1, 20)
        ]
        self.white_score = 0
        self.black_score = 0

    def __getitem__(self, location):
        letter = location[0].lower()
        letter_index = ord(letter) - 97
        num_index = location[1] - 1
        return self.board_array[num_index][letter_index]

    def __setitem__(self, location, value):
        letter = location[0].lower()
        letter_index = ord(letter) - 97
        num_index = location[1] - 1
        self.board_array[num_index][letter_index] = value

    def __repr__(self):
        return self.print_board()

    def print_board(self):
        return_str = '   a b c d e f g h i j k l m n o p q r s\n'
        for i, row in enumerate(self.board_array):
            return_str += '{0: <3}'.format(i+1)
            for col in row:
                if col == 1:
                    value = 'O'
                elif col == -1:
                    value = 'X'
                else:
                    value = '_'
                return_str += '{0: <1} '.format(value)
            return_str += '\n'

        return_str += '\nPlayer 1 (X): {}\nPlayer 2 (O): {}\n\nPlayer {}\'s Move (e.g. a1, b3, d2): '.format(
            self.white_score,
            self.black_score,
            2 - int(self.black_to_move)
        )

        return return_str


class Game:
    def __init__(self):
        self.board = Board()
        self.move_list = []
        self.board_list = []

    def get_dead_piece_locations(self):
        dead_piece_locations = []
        for location in self.board.all_locations:
            if self.board[location]:
                self.visited_pieces = []
                if not self.is_piece_alive(location):
                    dead_piece_locations += self.visited_pieces

        return dead_piece_locations

    def is_piece_alive(self, piece_location):
        self.visited_pieces.append(piece_location)

        if self.board.black_to_move:
            player_piece_value = -1
            opponent_piece_value = 1
        else:
            player_piece_value = 1
            opponent_piece_value = -1

        if self.board[piece_location] == player_piece_value:
            return True

        (letter, number) = piece_location
        neighbor_location_list = [(chr(ord(letter) + 1), number),
                                  (chr(ord(letter) - 1), number),
                                  (letter, number + 1),
                                  (letter, number - 1)]

        # Filter out neighbors that are outside defined board
        neighbor_location_list = [
            neighbor for neighbor in neighbor_location_list
            if (ord(neighbor[0]) >= ord('a') and ord(neighbor[0]) <= ord('s')
                and neighbor[1] >= 1 and neighbor[1] <= 19)
        ]

        for neighbor_location in neighbor_location_list:
            if self.board[neighbor_location] == 0:
                return True
            elif self.board[neighbor_location] == player_piece_value:
                continue
            elif self.board[neighbor_location] == opponent_piece_value:
                if (neighbor_location not in self.visited_pieces and
                        self.is_piece_alive(neighbor_location)):
                    return True
            else:
                raise Exception('Invalid board.')

        return False

    def remove_dead_pieces(self):
        for location in self.get_dead_piece_locations():
            if self.board[location] == -1:
                self.board.white_score += 1
            elif self.board[location] == 1:
                self.board.black_score += 1

            self.board[location] = 0

    def move(self, player_move_str):
        player_move = Move(player_move_str)
        if self.board[player_move.location]:
            return 'Illegal move.  Piece is already at this location. Try again: '
            # raise Exception('Illegal move.  Piece is already at this location.')

        if self.board.black_to_move:
            self.board[player_move.location] = -1
        else:
            self.board[player_move.location] = 1

        self.remove_dead_pieces()
        self.board.black_to_move = not self.board.black_to_move

        if player_move.location in self.get_dead_piece_locations():
            self.board.black_to_move = not self.board.black_to_move
            self.board[player_move.location] = 0
            return 'Illegal Move.  Piece is committing suicide. Try again: '
            # raise Exception('Illegal Move.  Piece is committing suicide.')

        if self.board.board_array in self.board_list:
            self.board.black_to_move = not self.board.black_to_move
            self.board[player_move.location] = 0
            return 'Illegal Move. This position has already occurred. Try again: '
            # raise Exception('Illegal Move. This position has already occurred.')

        self.move_list.append(player_move)
        self.board_list.append(deepcopy(self.board.board_array))
        return self.board.print_board()

