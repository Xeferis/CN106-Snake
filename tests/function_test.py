import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from snake import *


@pytest.fixture
def test_snake():
    s = snake()
    return s

@pytest.fixture
def test_board(test_snake):
    b = board(snake=test_snake)
    return b





