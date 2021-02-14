import unittest
from unittest import TestCase

from main import Board, Position, MoveOffBoardError


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

    def test_invalid_move_goes_nowhere(self):
        self.Board.move_white_rook_1(Position(7, 7))

        r1 = self.Board.get_white_rook_1()
        self.assertEqual(Position(0, 0), r1.Position)

    def test_moving_on_board_does_not_throw_exception(self):
        self.Board.move_white_rook_1(Position(0, 7))

    def test_moving_off_board_throws_exception(self):
        with self.assertRaises(MoveOffBoardError):
            self.Board.move_white_rook_1(Position(0, 8))

        #self.assertRaises(MoveOffBoardError(), self.Board.move_white_rook_1, Position(0,10))
        #self.Board.move_white_rook_1(Position(0, 9))
