from board import Board, TicTacToeBoard, ConnectFourBoard
from player import Player


def test_render_board():
    '''
    board: [['A', 'B'], ['B', 'A']]
    render: |'B'|'A'|
            |'A'|'B'|
            GAMEOVER? False

    '''
    player_a = Player("A")
    player_b = Player("B")
    board = Board([[player_a, player_b], [player_b, player_a]])
    assert board.render() == [['|', 'B', '|', 'A', '|'],
                              ['|', 'A', '|', 'B', '|'],
                              ["GAMEOVER? False\n"]]

    '''
    board: [['A', -], ['C', 'A']]
    render: | - | A |
            | A | C |
            GAMEOVER? True\n
    '''
    player_c = Player("C")
    board = Board([[player_a, None], [player_c, player_a]])
    board._gameover = True
    assert board.render() == [['|', '-', '|', 'A', '|'],
                              ['|', 'A', '|', 'C', '|'],
                              ["GAMEOVER? True\n"]]

    '''
    board: [[None, None, None], [None, None, None], [None, None, None]]
    render:  | - | - | - |
             | - | - | - |
             | - | - | - |
            GAMEOVER? False\n
    '''
    board = Board([[None, None, None], [None, None, None], [None, None, None]])
    assert board.render() == [['|', '-', '|', '-', '|', '-', '|'],
                              ['|', '-', '|', '-', '|', '-', '|'],
                              ['|', '-', '|', '-', '|', '-', '|'],
                              ["GAMEOVER? False\n"]]


def test_get_open_locations():
    '''
    board:  - | -
            - - -
            - | -
    '''
    board = Board([[None, None], [None, None]])
    assert set(board.get_open_locations()) == set([
        (0, 0), (0, 1), (1, 0), (1, 1)])

    '''
    board:  A | -
            - - -
            - | -
    '''
    board = Board([["A", None], [None, None]])
    assert set(board.get_open_locations()) == set([(0, 1), (1, 0), (1, 1)])

    '''
    board:  A | B
            - - -
            C | A
    '''
    board = Board([["A", "C"], ["B", "A"]])
    assert set(board.get_open_locations()) == set()


def test_is_gameover():
    board = Board()
    assert not board.is_gameover()
    # if member variable set, should always return True
    board._gameover = True
    assert board.is_gameover()


class CompleteBoard(Board):

    def validate_matrix(self, x_pos, y_pos, player):
        assert not self._gameover
        self._gameover = True


def test_set_location_updates_the_matrix():
    matrix = [[None]]
    board = Board(matrix)
    player_a = Player("A")
    board.set_location(0, 0, player_a)
    assert matrix[0][0] == player_a

    matrix = [[None, None], [None, None]]
    board = Board(matrix)
    player_b = Player("B")
    board.set_location(1, 0, player_b)
    assert matrix[1][0] == player_b

    board.set_location(1, 1, player_a)
    assert matrix[1][1] == player_a

    # assert set location validates the matrix
    board = CompleteBoard([[None]])
    board.set_location(0, 0, 'A')
    assert board._gameover


def test_tic_tac_toe_set_location_validates_matrix():
    # row
    board = TicTacToeBoard([['A', 'B', None],
                            ['A', 'B', None],
                            [None, None, None]])
    board.set_location(2, 0, 'A')
    assert board._gameover == True
    assert board._winner == 'A'

    # row
    board = TicTacToeBoard([['A', 'B', None],
                            ['A', 'B', None],
                            [None, None, None]])
    board.set_location(2, 1, 'B')
    assert board._gameover == True
    assert board._winner == 'B'

    # row
    board = TicTacToeBoard([['A', 'B', 'C'],
                            ['A', 'B', 'C'],
                            [None, None, None]])
    board.set_location(2, 2, 'C')
    assert board._gameover == True
    assert board._winner == 'C'

    # column
    board = TicTacToeBoard([['A', 'A', None],
                            ['A', 'B', None],
                            ['B', None, None]])
    board.set_location(0, 2, 'A')
    assert board._gameover == True
    assert board._winner == 'A'

    # column
    board = TicTacToeBoard([['A', 'A', None],
                            ['B', 'B', None],
                            ['B', None, None]])
    board.set_location(1, 2, 'B')
    assert board._gameover == True
    assert board._winner == 'B'

    # column
    board = TicTacToeBoard([['A', 'A', None],
                            ['B', 'B', None],
                            ['C', 'C', None]])
    board.set_location(2, 2, 'C')
    assert board._gameover == True
    assert board._winner == 'C'

    # diagonal
    board = TicTacToeBoard([['A', 'B', 'B'],
                            ['A', 'A', 'B'],
                            ['B', None, None]])
    board.set_location(2, 2, 'A')
    assert board._gameover == True
    assert board._winner == 'A'

    # diagonal
    board = TicTacToeBoard([['A', 'A', None],
                            ['A', 'B', None],
                            ['B', None, None]])
    board.set_location(0, 2, 'B')
    assert board._gameover == True
    assert board._winner == 'B'

    # cats
    board = TicTacToeBoard([[None, None, None],
                            [None, None, None],
                            [None, None, None]])
    board._move_count = 8
    board.set_location(0, 0, 'A')
    assert board._gameover == True
    assert not board._winner


def test_connect_four_open_locations():
    board = ConnectFourBoard([[None, None],
                              [None, None],
                              [None, None]])
    assert set(board.get_open_locations()) == set([(0, 0), (1, 0), (2, 0)])

    board = ConnectFourBoard([[None, None],
                              ['A', None],
                              ['B', 'A']])
    assert set(board.get_open_locations()) == set([(0, 0), (1, 1)])


def test_connect_four_set_location():
    # row
    board = ConnectFourBoard([['B', None, None, None, None, None],
                              ['B', None, None, None, None, None],
                              ['A', 'B', None, None, None, None],
                              ['A', None, None, None, None, None],
                              ['A', None, None, None, None, None],
                              [None, None, None, None, None, None]])
    board.set_location(5, 0, 'A')
    assert board._gameover == True
    assert board._winner == 'A'

    # row
    board = ConnectFourBoard([['B', 'B', None, None, None, None],
                              ['B', 'A', None, None, None, None],
                              ['A', 'A', None, None, None, None],
                              ['A', 'A', None, None, None, None],
                              ['A', None, None, None, None, None],
                              ['B', 'B', None, None, None, None]])
    board.set_location(4, 1, 'A')
    assert board._gameover == True
    assert board._winner == 'A'

    # column
    board = ConnectFourBoard([['B', 'B', 'B', None, None, None],
                              ['B', 'A', 'A', None, None, None],
                              ['A', 'A', None, None, None, None],
                              ['A', 'A', None, None, None, None],
                              ['A', 'B', None, None, None, None],
                              ['B', 'B', None, None, None, None]])
    board.set_location(0, 3, 'B')
    assert board._gameover == True
    assert board._winner == 'B'

    # column
    board = ConnectFourBoard([['B', 'B', 'B', None, None, None],
                              ['A', 'A', 'A', None, None, None],
                              ['A', 'A', None, None, None, None],
                              ['A', 'A', None, None, None, None],
                              ['A', 'B', None, None, None, None],
                              ['B', 'B', None, None, None, None]])
    board.set_location(1, 3, 'A')
    assert board._gameover == True
    assert board._winner == 'A'

    # diagonal
    board = ConnectFourBoard([['A', 'B', 'B', None, None, None],
                              ['A', 'A', 'A', None, None, None],
                              ['A', 'A', 'A', None, None, None],
                              ['A', 'B', 'A', None, None, None],
                              ['A', 'B', 'B', None, None, None],
                              ['B', 'B', None, None, None, None]])
    board.set_location(3, 3, 'A')
    assert board._gameover == True
    assert board._winner == 'A'

    # diagonal
    board = ConnectFourBoard([['B', 'B', 'B', None, None, None],
                              ['A', 'A', 'A', None, None, None],
                              ['A', 'A', None, None, None, None],
                              ['A', 'B', 'A', None, None, None],
                              ['A', 'B', 'B', None, None, None],
                              ['B', 'B', None, None, None, None]])
    board.set_location(4, 3, 'A')
    assert board._gameover == True
    assert board._winner == 'A'

    # diagonal
    board = ConnectFourBoard([['B', 'B', 'B', None, None, None],
                              ['A', 'A', 'A', None, None, None],
                              ['A', 'A', None, 'A', None, None],
                              ['A', 'B', 'A', None, 'A', None],
                              ['A', 'B', 'B', None, None, None],
                              ['B', 'B', None, None, None, None]])
    board.set_location(4, 5, 'A')
    assert board._gameover == True
    assert board._winner == 'A'

    # diagonal
    board = ConnectFourBoard([['A', 'B', 'A', None, None, None],
                              ['A', 'B', 'A', None, None, None],
                              ['A', None, None, None, None, None],
                              ['B', 'B', 'B', None, None, None],
                              ['A', 'A', 'B', None, None, None],
                              ['B', 'A', 'B', 'A', 'B', 'A']])
    board.set_location(4, 3, 'A')
    assert board._gameover == False
    assert not board._winner

    # reverse diagonal
    board = ConnectFourBoard([['A', 'B', 'B', None, None, None],
                              ['A', 'A', 'A', None, None, None],
                              ['A', 'A', 'A', None, None, None],
                              ['A', 'B', 'A', None, None, None],
                              ['A', 'B', 'B', None, None, None],
                              ['B', 'B', None, None, None, None]])
    board.set_location(0, 3, 'A')
    assert board._gameover == True
    assert board._winner == 'A'

    # reverse diagonal
    board = ConnectFourBoard([['A', 'B', 'B', None, None, None],
                              ['A', 'B', 'A', None, None, None],
                              ['A', 'A', 'A', None, None, None],
                              ['A', 'A', 'A', None, None, None],
                              ['A', 'B', 'B', None, None, None],
                              ['B', 'B', None, None, None, None]])
    board.set_location(1, 3, 'A')
    assert board._gameover == True
    assert board._winner == 'A'

    # reverse diagonal
    board = ConnectFourBoard([[None, None, None, None, None, None],
                              [None, None, None, None, None, None],
                              [None, None, None, None, 'A', None],
                              [None, None, None, 'A', None, None],
                              [None, None, 'A', None, None, None],
                              [None, None, None, None, None, None]])
    board.set_location(5, 1, 'A')
    assert board._gameover == True
    assert board._winner == 'A'
