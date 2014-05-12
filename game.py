import argparse

from engine import ConnectionGameEngine
from player import Player
from board import TicTacToeBoard, ConnectFourBoard, MegaTicTacToe


class Games(object):

    TIC_TAC_TOE = "t3"
    CONNECT_FOUR = "c4"
    MEGA_TTT = "mt3"


def run(game):
    # Should be a factory
    if game == Games.TIC_TAC_TOE:
        players = [Player('A'), Player('B')]
        board = TicTacToeBoard()
    elif game == Games.CONNECT_FOUR:
        players = [Player('A'), Player('B')]
        board = ConnectFourBoard()
    else:
        players = [Player('A'), Player('B'), Player('C'), Player('D')]
        board = MegaTicTacToe()
    engine = ConnectionGameEngine(players, board)
    engine.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "game", help="Which game do you want to run?",
        choices=[Games.TIC_TAC_TOE, Games.CONNECT_FOUR, Games.MEGA_TTT])
    args = parser.parse_args()
    run(args.game)
