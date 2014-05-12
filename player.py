from random import randint


class Player(object):

    def __init__(self, symbol=None):
        self.symbol = symbol

    def choose_open_location(self, board):
        open_locations = board.get_open_locations()
        assert open_locations
        return open_locations[randint(0, len(open_locations) - 1)]

    def render(self):
        return self.symbol
