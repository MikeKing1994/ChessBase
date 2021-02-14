import unittest
from unittest import TestCase

from main import Board, Position, MoveOffBoardError, RookCanOnlyMoveInOneAxisError


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.Board = Board()


class TestInit(TestBoard):
    def test_initial_pieces(self):
        self.assertEqual(4, len(self.Board.Pieces))

    def test_get_all_white_pieces(self):
        all_white = len(self.Board.get_all_white_pieces())
        self.assertEqual(2, all_white)


class TestBoard(TestBoard):
    def test_basic_capture(self):
        self.Board.move_white_rook_1(Position(0, 7))

        self.assertEqual(False, self.Board.get_white_rook_1().Taken)
        self.assertEqual(True, self.Board.get_black_rook_1().Taken)

    def test_moving_on_board_does_not_throw_exception(self):
        self.Board.move_white_rook_1(Position(0, 7))

    def test_moving_off_board_throws_exception(self):
        with self.assertRaises(MoveOffBoardError):
            self.Board.move_white_rook_1(Position(0, 8))

    def test_moving_Rook_on_on_one_axis_does_not_throw_exception(self):
        self.Board.move_white_rook_1(Position(0, 7))

    def test_moving_Rook_invalidly_throws_exception(self):
        with self.assertRaises(RookCanOnlyMoveInOneAxisError):
            self.Board.move_white_rook_1(Position(2, 2))
