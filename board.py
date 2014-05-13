import math


class Board(object):

    _connection_length = 0
    _location_matrix = [[]]
    _board_size = 0

    def __init__(self, matrix=None):
        self._gameover = False
        self._winner = None
        self._move_count = 0
        if not matrix:
            self._location_matrix = [[None for i in xrange(self._board_size)]
                                     for o in xrange(self._board_size)]
        else:
            self._location_matrix = matrix
            self._board_size = len(matrix)

    def check_column(self, x_pos, y_pos, player):
        count = 0
        for index in xrange(self._board_size):
            if self._location_matrix[x_pos][index] != player:
                count = 0
            else:
                count += 1
            if count == self._connection_length:
                return player

    def check_row(self, x_pos, y_pos, player):
        count = 0
        for index in xrange(self._board_size):
            if self._location_matrix[index][y_pos] != player:
                count = 0
            else:
                count += 1
            if count == self._connection_length:
                return player

    def check_diagonal(self, x_pos, y_pos, player):
        y_offset = y_pos - x_pos
        count = 0
        for index in xrange(self._board_size):
            y_pos = index + y_offset
            if y_pos < 0:
                continue
            elif y_pos >= self._board_size:
                return
            elif self._location_matrix[index][y_pos] != player:
                count = 0
                continue
            else:
                count += 1
            if count == self._connection_length:
                return player

    def check_reverse_diagonal(self, x_pos, y_pos, player):
        # y = -x + y_pos + x_pos
        count = 0
        y_offset = y_pos + x_pos
        for index in xrange(self._board_size):
            y_pos = -index + y_offset
            if y_pos >= self._board_size:
                count = 0
                continue
            elif y_pos < 0:
                return
            elif self._location_matrix[index][y_pos] != player:
                count = 0
                continue
            else:
                count += 1
            if count == self._connection_length:
                return player

    def check_cats(self, x_pos, y_pos, player):
        if self._move_count == math.pow(self._board_size, 2):
            self._gameover = True

    def validate_matrix(self, x_pos, y_pos, player):
        checks = [self.check_column, self.check_row, self.check_diagonal,
                  self.check_reverse_diagonal, self.check_cats]
        for check in checks:
            winner = check(x_pos, y_pos, player)
            if winner:
                self._winner = winner
                self._gameover = True
                return

    def render(self):
        lines = []
        line = []
        for y_index in reversed(xrange(self._board_size)):
            line.append("|")
            for x_index, y_values in enumerate(self._location_matrix):
                player = y_values[y_index]
                line.append(player.render() if player else "-")
                line.append("|")
            lines.append(line)
            line = []
        lines.append(["GAMEOVER? %s\n" % self._gameover])
        for line in lines:
            print " ".join(line)
        return lines

    def get_open_locations(self):
        open_locations = []
        for x_pos, y in enumerate(self._location_matrix):
            for y_pos, player in enumerate(y):
                if not player:
                    open_locations.append((x_pos, y_pos))
        return open_locations

    def is_gameover(self):
        return self._gameover

    def winner(self):
        return self._winner

    def set_location(self, x_pos, y_pos, player):
        assert x_pos >= 0 and x_pos < self._board_size
        assert y_pos >= 0 and y_pos < self._board_size

        self._location_matrix[x_pos][y_pos] = player
        self._move_count += 1

        self.validate_matrix(x_pos, y_pos, player)


class TicTacToeBoard(Board):

    _connection_length = 3
    _board_size = 3


class ConnectFourBoard(Board):

    _connection_length = 4
    _board_size = 6

    def get_open_locations(self):
        open_locations = []
        for x_index, y_values in enumerate(self._location_matrix):
            for y_index, value in enumerate(y_values):
                if not value:
                    open_locations.append((x_index, y_index))
                    break
        return open_locations


class MegaTicTacToe(Board):

    _connection_length = 3
    _board_size = 8

    def check_column(self, x_pos, y_pos, player):
        pass

    def check_row(self, x_pos, y_pos, player):
        pass
