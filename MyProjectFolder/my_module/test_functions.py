import pytest

from functions import *

def test_follow_bot():
    assert FollowBot
    fbot = FollowBot(character = 1279)
    assert isinstance(fbot, Bot)
    assert fbot.follow() == fbot.position
    fbot.grid_size = 5
    fbot.move()
    assert fbot.position != [0, 0]

def test_eat():
    bots = [FollowBot(), WanderBot()]
    bots[0].position = [1, 1]
    bots[1].position = [0, 1]
    food_list = [[0, 1], [0, 0]]
    assert eat(bots, food_list) is None
    eat(bots, food_list)
    assert food_list == [[0, 0]]
    