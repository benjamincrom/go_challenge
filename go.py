'''
go.py --
'''

from collections import namedtuple

FullMove = namedtuple('FullMove', 'black_move white_move')

def char_range(c1, c2):
    for c in xrange(ord(c1), ord(c2)):
        yield chr(c)


class Move:
    def __init__(self, move_str):
        self.letter = move_str[0].lower()
        self.number = int(move_str[1:])
        self.location = (self.letter, self.number)

    def __repr__(self):
        return "Move('{}{}')".format(self.letter, self.number)


class Board:
    def __init__(self):
        self.board_array = [[0 for _ in range(19)] for _ in range(19)]
        self.full_move_list = []
        self.black_to_move = True
        self.black_half_move = None

    def __getitem__(self, location):
        letter = location[0].lower()
        letter_index = ord(letter) - 97
        num_index = location[1] - 1
        return self.board_array[letter_index][num_index]

    def __setitem__(self, location, value):
        letter = location[0].lower()
        letter_index = ord(letter) - 97
        num_index = location[1] - 1
        self.board_array[letter_index][num_index] = value

    def __repr__(self):
        return_str = ''
        for row in self.board_array:
            for col in row:
                return_str += '{0: <3} '.format(col)
            return_str += '\n'

        return return_str


class Game:
    def __init__(self):
        self.board = Board()
        self.move_list = []
        self.white_score = 0
        self.black_score = 0

    def get_dead_piece_locations(self):
        dead_piece_location_list = []
        for c in char_range('a', '['):
            for i in range(1, 20):
                coordinate = (c, i)
                liberties = [self.board[(chr(ord(c) + 1), i)],
                             self.board[(chr(ord(c) - 1), i)],
                             self.board[(c, i + 1)],
                             self.board[(c, i - 1)]]

                all(liberties)

    def remove_dead_pieces(self, dead_piece_locations):
        pass

    def move(self, player_move):
        if self.board[player_move.location]:
            raise Exception('Illegal move')

        if self.board.black_to_move:
            self.board[player_move.location] = -1
            self.board.black_half_move = player_move
            self.board.black_to_move = False
        else:
            self.board[player_move.location] = 1
            self.move_list.append(
                FullMove(
                    black_move=self.board.black_half_move,
                    white_move=player_move
                )
            )
            self.board.black_half_move = None
            self.board.black_to_move = True

        dead_piece_locations = self.get_dead_piece_locations()
        if player_move.location in dead_piece_locations:
            raise Exception('Illegal Move')
