import unittest
from unittest import TestCase

from puppeteer import get_chess_dot_com_square_name_from_position
from main import Position


class TestBasic(unittest.TestCase):
    def setUp(self):
        ()

    def test_get_chess_dot_com_square_name(self):
        pos = Position(4, 1)
        ret = get_chess_dot_com_square_name_from_position(pos)
        self.assertEqual("square-52", ret)
