from mock import patch, Mock

from player import Player


def test_player_renders_symbol():
    player = Player("SS")
    assert player.render() == "SS"


@patch("player.randint")
def test_player_chooses_location_randomly(randint):
    attrs = {"get_open_locations.return_value": [1, 2, 3]}
    board = Mock(**attrs)
    randint.return_value = 2
    player = Player("p")
    assert player.choose_open_location(board)
