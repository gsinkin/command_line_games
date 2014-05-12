import logging

logger = logging.getLogger(__name__)


class ConnectionGameEngine(object):

    def __init__(self, players, board):
        self.players = players
        self.board = board

    def run(self):
        logger.debug("Starting game")
        while not self.board.is_gameover():
            for player in self.players:
                x_pos, y_pos = player.choose_open_location(self.board)
                self.board.set_location(x_pos, y_pos, player)
                self.board.render()
                if self.board.is_gameover():
                    break
        logger.debug("Game over")
        return True
