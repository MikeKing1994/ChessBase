import unittest
from unittest import TestCase
from puppeteer import get_chess_dot_com_square_name_from_position, read_board, start_game_against_jimmy_on_chess_dot_com, move_piece_on_chess_dot_com
import time
from main import Position
from file_logging import *


class TestBasic(unittest.TestCase):
    def setUp(self):
        set_up_complete = True


class TestLogging(TestBasic):
    def test_file_name_generation(self):
        file_name = generate_log_file_name()
        self.assertTrue(file_name.endswith(".log"))


class Tests(TestBasic):
    def test_start_game_and_read_starting_board(self):
        game_driver = start_game_against_jimmy_on_chess_dot_com()
        b = read_board(game_driver)
        self.assertEqual(32, len(b.Pieces))

    def test_get_chess_dot_com_square_name(self):
        pos = Position(4, 1)
        ret = get_chess_dot_com_square_name_from_position(pos)
        self.assertEqual("square-52", ret)

    def test_start_game_play_one_move_and_read_board(self):
        game_driver = start_game_against_jimmy_on_chess_dot_com()
        move_piece_on_chess_dot_com(game_driver, Position(0, 1), Position(0, 3))
        time.sleep(3)
        b = read_board(game_driver)
        self.assertEqual(32, len(b.Pieces))


