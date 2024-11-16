import os
import sys
import pytest
from unittest.mock import Mock
import tkinter as tk

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from snake import *

@pytest.fixture
def test_zone():
    z = zone(10, 10, 10, 10)
    return z

@pytest.fixture
def test_snake():
    s = snake()
    return s


@pytest.fixture
def test_board(test_snake):
    b = board(snake=test_snake)
    return b


def test_add_deadzone(test_board):
    test_board._add_deadzone(0, 0, 10, 10)
    assert test_board.deadzones[-1].get_start() == (0, 0)
    assert test_board.deadzones[-1].get_end() == (10, 10)


def test_check_deadzone(test_board):
    test_board._add_deadzone(0, 0, 10, 10)
    assert test_board._check_deadzone(5, 5) == True


def test_check_food_position(test_board):
    test_board.food = [food(5, 5)]
    assert test_board._check_food_position(5, 5) == True


def check_snake_position(test_board):
    test_board.snake = snake()
    test_board.snake.x = 5
    test_board.snake.y = 5
    assert test_board.check_snake_position(5, 5) == True


def test_progression(test_board):
    test_board.points = 10
    test_board.points2win = 10
    test_board._progression()
    assert test_board.won == True


def test_earn_points(test_board):
    assert test_board.points == 0
    test_board.points = 5
    test_board._progression()
    assert test_board.points == 11
    assert test_board.level == 2


def test_generate_point(test_board):
    x, y = test_board._generate_point()
    assert x >= 10 and x <= 790
    assert y >= 10 and y <= 590


def test_generate_food(test_board):
    test_board._generate_food()
    assert len(test_board.food) == 2
    for f in test_board.food:
        assert f.x >= 10 and f.x <= 500
        assert f.y >= 10 and f.y <= 500
        assert not test_board._check_deadzone(f.x, f.y), f"Deadzone at {f.x}, {f.y}"
        assert not test_board._check_snake_position(f.x, f.y), f"Snake at {f.x}, {f.y}"


@pytest.mark.skip(reason="Not Testable yet!")
def test_control(test_board):
    return True


def test_wall_collision(test_board):
    test_board.snake.x = -1
    test_board.snake.y = -1
    assert test_board._wall_collision() == True
    test_board.snake.x = 800
    test_board.snake.y = 600
    assert test_board._wall_collision() == True
    test_board.snake.x = 400
    test_board.snake.y = 300
    assert test_board._wall_collision() == False


def test_food_collision(test_board):
    test_board._generate_food(1)
    test_board.snake.move("d")
    test_food = test_board.food[0]
    fx, fy = test_food.get_pos()
    test_board.snake.x = fx
    test_board.snake.y = fy
    assert test_board._food_collision() == True
    test_board.snake.x = 10
    test_board.snake.y = 10
    assert test_board._food_collision() == False


def test_tail_collision(test_board):
    test_board.snake.y = 10
    test_board.snake.x = 10

    test_board.snake.move("d")
    test_board.snake.move("d")

    assert test_board.snake.get_pos() == (10, 30)
    assert test_board.snake.length == 0
    test_board.snake.grow()

    assert test_board.snake.length == 1

    test_board.snake.move("d")
    test_board.snake.move("d")

    assert test_board.snake.get_pos() == (10, 50)

    test_board.snake.move("u")

    assert test_board.snake.get_pos() == (10, 40)
    assert test_board._tail_collision()

def test_body_update(test_snake):
    test_snake.update(10, 10)
    assert test_snake.x == 10
    assert test_snake.y == 10

def test_body_get_pos(test_snake):
    assert test_snake.get_pos() == (0, 0)

def test_snake_move(test_snake):
    test_snake.move("u")
    assert test_snake.get_pos() == (0, -10)
    test_snake.move("d")
    assert test_snake.get_pos() == (0, 0)
    test_snake.move("l")
    assert test_snake.get_pos() == (-10, 0)
    test_snake.move("r")
    assert test_snake.get_pos() == (0, 0)

def test_snake_grow(test_snake):
    test_snake.last.append((0, 0))
    test_snake.grow()
    assert test_snake.length == 1
    test_snake.last.append((0, 0))
    test_snake.grow()
    assert test_snake.length == 2

def test_zone_get_start(test_zone):
    assert test_zone.get_start() == (10, 10)

def test_zone_get_end(test_zone):
    assert test_zone.get_end() == (20, 20)
