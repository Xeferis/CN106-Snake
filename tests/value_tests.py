import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from snake import *


def test_board():
    s = snake()
    b = board(snake=s)
    assert b.snake == s
    assert b.width == 500
    assert b.height == 500
    assert b.food == []
    assert b.game_over == False


def test_snake():
    s = snake()
    assert s.x == 0
    assert s.y == 0
    assert s.length == 0
    assert s.last == []
    assert s.width == 10
    assert s.height == 10


def test_body():
    b = body()
    assert b.x == 0
    assert b.y == 0
    assert b.height == 10
    assert b.width == 10


def test_food():
    f = food(10, 10)
    assert f.x == 10
    assert f.y == 10
    assert f.height == 10
    assert f.width == 10
