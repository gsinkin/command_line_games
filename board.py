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

    def validate_matrix(self, x_pos, y_pos, player):
        pass

    def render(self):
        lines = []
        line = []
        for y_index in reversed(xrange(self._board_size)):
            for x_index, y_values in enumerate(self._location_matrix):
                player = y_values[y_index]
                line.append(player.render() if player else "-")
                if x_index < self._board_size - 1:
                    line.append("|")
            lines.append(line)
            line = []
            if y_index > 0:
                for player in xrange((self._board_size * 2) - 1):
                    line.append("-")
                lines.append(line)
                line = []
        lines.append(["GAMEOVER? %s" % self._gameover])
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
        assert x_pos < self._board_size
        assert y_pos < self._board_size

        self._location_matrix[x_pos][y_pos] = player
        self._move_count += 1

        self.validate_matrix(x_pos, y_pos, player)


class TicTacToeBoard(Board):

    _connection_length = 3
    _board_size = 3

    def validate_matrix(self, x_pos, y_pos, player):
        # check column
        for index in xrange(self._board_size):
            if self._location_matrix[x_pos][index] != player:
                break
            if index == self._board_size - 1:
                self._gameover = True
                self._winner = player
                return

        # check row
        for index in xrange(self._board_size):
            if self._location_matrix[index][y_pos] != player:
                break
            if index == self._board_size - 1:
                self._gameover = True
                self._winner = player
                return

        # check diagonal
        for index in xrange(self._board_size):
            if self._location_matrix[index][index] != player:
                break
            if index == self._board_size - 1:
                self._gameover = True
                self._winner = player
                return

        # check diagonal
        for index in xrange(self._board_size):
            y_pos = self._board_size - index - 1
            if self._location_matrix[index][y_pos] != player:
                break
            if index == self._board_size - 1:
                self._gameover = True
                self._winner = player
                return

        # cats game
        if self._move_count == math.pow(self._board_size, 2):
            self._gameover = True


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

    def validate_matrix(self, x_pos, y_pos, player):
        # this algorithm sucks. needs improvement
        # check column
        count = 0
        for index in xrange(self._board_size):
            if self._location_matrix[x_pos][index] != player:
                count = 0
            else:
                count += 1
            if count == self._connection_length:
                self._gameover = True
                self._winner = player
                return

        # check row
        count = 0
        for index in xrange(self._board_size):
            if self._location_matrix[index][y_pos] != player:
                count = 0
            else:
                count += 1
            if count == self._connection_length:
                self._gameover = True
                self._winner = player
                return

        # check diagonal
        diff = self._board_size - self._connection_length + 1
        for x_offset in xrange(0, diff):
            for y_offset in xrange(0, diff):
                count = 0
                for index in xrange(self._board_size - max(x_offset, y_offset)):
                    if self._location_matrix[x_offset + index][y_offset + index] != player:
                        count = 0
                    else:
                        count += 1
                    if count == self._connection_length:
                        self._gameover = True
                        self._winner = player
                        return

        # check reverse diagonal
        for x_offset in xrange(0, diff):
            for y_offset in xrange(0, diff):
                count = 0
                for index in xrange(self._board_size - max(x_offset, y_offset)):
                    if self._location_matrix[index + x_offset][self._board_size - 1 - y_offset - index] != player:
                        count = 0
                    else:
                        count += 1
                    if count == self._connection_length:
                        self._gameover = True
                        self._winner = player
                        return

        # cats game
        if self._move_count == math.pow(self._board_size, 2):
            self._gameover = True


class MegaTicTacToe(Board):

    _connection_length = 3
    _board_size = 8

    def validate_matrix(self, x_pos, y_pos, player):
        # check diagonal
        diff = self._board_size - self._connection_length + 1
        for x_offset in xrange(0, diff):
            for y_offset in xrange(0, diff):
                count = 0
                for index in xrange(self._board_size - max(x_offset, y_offset)):
                    if self._location_matrix[x_offset + index][y_offset + index] != player:
                        count = 0
                    else:
                        count += 1
                    if count == self._connection_length:
                        self._gameover = True
                        self._winner = player
                        return

        # check reverse diagonal
        for x_offset in xrange(0, diff):
            for y_offset in xrange(0, diff):
                count = 0
                for index in xrange(self._board_size - max(x_offset, y_offset)):
                    if self._location_matrix[index + x_offset][self._board_size - 1 - y_offset - index] != player:
                        count = 0
                    else:
                        count += 1
                    if count == self._connection_length:
                        self._gameover = True
                        self._winner = player
                        return

        # cats game
        if self._move_count == math.pow(self._board_size, 2):
            self._gameover = True
