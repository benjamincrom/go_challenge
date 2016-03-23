'''
go.py --
'''

from collections import namedtuple

FullMove = namedtuple('FullMove', 'black_move white_move')

def char_range(c1, c2):
    for c in xrange(ord(c1), ord(c2)):
        yield chr(c)

def convert_location_to_tuple(location):
    ''' Accepts string 'a2' or tuple ('a', 2) '''
    if type(location) is str:
        letter = location[0].lower()
        number = int(location[1:])
        location = (letter, number)
    elif type(location) is tuple:
        letter = str(location[0]).lower()
        number = int(location[1])
        location = (letter, number)
    else:
        raise Exception('Not a valid location.')

    return location

def convert_location_to_index_tuple(location):
    location_tuple = convert_location_to_tuple(location)
    letter_index = ord(location_tuple[0]) - 97
    num_index = location_tuple[1] - 1
    return (letter_index, num_index)


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
        self.all_locations = [
            (c, i) for c in char_range('a','t') for i in range(1, 20)
        ]

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

        if self.board[piece_location] == opponent_piece_value:
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
            elif self.board[neighbor_location] == opponent_piece_value:
                continue
            elif self.board[neighbor_location] == player_piece_value:
                if (neighbor_location not in self.visited_pieces and
                        self.is_piece_alive(neighbor_location)):
                    return True
            else:
                raise Exception('Invalid board.')

        return False

    def remove_dead_pieces(self, dead_piece_locations):
        for location in dead_piece_locations:
            if self.board[location] == -1:
                self.white_score += 1
            elif self.board[location] == 1:
                self.black_score += 1

            self.board[location] = 0

    def move(self, player_move_str):
        player_move = Move(player_move_str)
        if self.board[player_move.location]:
            raise Exception('Illegal move.  Piece is already at this location.')

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
            raise Exception('Illegal Move.  Piece is committing suicide.')

        self.remove_dead_pieces(dead_piece_locations)
