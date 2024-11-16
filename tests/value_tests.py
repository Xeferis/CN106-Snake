import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from snake import *


def test_zone():
    z = zone(10, 10, 10, 10)
    assert z.x == 10
    assert z.y == 10
    assert z.width == 10
    assert z.height == 10


def test_board():
    s = snake()
    b = board(snake=s)
    assert b.snake == s
    assert b.width == 500
    assert b.height == 500
    assert b.food == []
    assert b.points2win == 100
    assert b.start_x == 500 // 2
    assert b.start_y == 500 // 2
    assert b.level == 1
    assert b.speed == 100
    assert b.points == 0
    assert b.won == False
    assert b.game_over == False


def test_food():
    f = food(10, 10)
    assert f.x == 10
    assert f.y == 10
    assert f.height == 10
    assert f.width == 10


def test_snake():
    s = snake()
    assert s.x == 0
    assert s.y == 0
    assert s.length == 0
    assert s.last == []
    assert s.direction == None
    assert s.tail == []
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
