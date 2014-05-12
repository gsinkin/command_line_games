from mock import Mock

from board import Board
from player import Player
from engine import ConnectionGameEngine


def test_run_does_nothing_on_gameover():
    # this is a silly test. meh
    board = Board()
    board._gameover = True
    base_engine = ConnectionGameEngine([], board)
    assert base_engine.run()
