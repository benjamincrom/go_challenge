'''
go.py --
'''

from collections import namedtuple

FullMove = namedtuple('FullMove', 'black_move white_move')


class Move:
    def __init__(self, move_str):
        self.letter = move_str[0].upper()
        self.number = int(move_str[1:])
        self.location = (self.letter, self.number)

    def __repr__(self):
        return '{}'.format(self.location)


class Board:
    def __init__(self):
        self.board_array = [[0 for _ in range(13)] for _ in range(13)]
        self.full_move_list = []
        self.black_to_move = True
        self.black_half_move = None

    def __getitem__(self, location):
        letter = location[0].upper()
        letter_index = ord(letter) - 65
        num_index = location[1] - 1
        return self.board_array[letter_index][num_index]

    def __setitem__(self, location, value):
        letter = location[0].upper()
        letter_index = ord(letter) - 65
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
        self.move_list = []
        self.board = Board()

    def move(self, player_move):
        if self.board.black_to_move:
            self.board.black_half_move = player_move
            self.board.black_to_move = False
            self.board[player_move.location] = -1
        else:
            self.move_list.append(
                FullMove(
                    black_move=self.board.black_half_move,
                    white_move=player_move
                )
            )
            self.board.black_half_move = None
            self.board.black_to_move = True
            self.board[player_move.location] = 1
