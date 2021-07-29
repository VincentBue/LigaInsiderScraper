from scraper import *
from copy import deepcopy

DEFAULT = Player('Alessandro Schöpf',
                    'Arminia Bielefeld',
                    'Mittelfeldspieler',
                    180,
                    [('28/7/2021', 180)],
                    3402070,
                    [('28/7/2021', 3402070)])

def test_not_update_twice():
    x = DEFAULT
    y = deepcopy(x)
    update_player(x, y)
    assert len(x.market_value_history) == 1, "Player got updated"

def test_update_pos():
    x = DEFAULT
    y = deepcopy(x)
    y.position = "Torhüter"
    y.last_modified = "-1"
    update_player(x, y)
    assert x.position == "Torhüter"