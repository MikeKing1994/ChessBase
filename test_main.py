import unittest
from unittest import TestCase

from main import (Board, Position, MoveOffBoardError, RookCanOnlyMoveInOneAxisError, MoveBlockedByPieceError, Rook,
                  King, Knight, MoveCausesYourKingToBeInCheckError)


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.Board = Board(None)


class TestInit(TestBoard):
    def test_initial_pieces(self):
        self.assertEqual(16, len(self.Board.Pieces))

    def test_get_all_white_pieces(self):
        all_white = len(self.Board.get_all_white_pieces())
        self.assertEqual(8, all_white)


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

    def test_moving_rook_on_on_one_axis_does_not_throw_exception(self):
        self.Board.move_white_rook_1(Position(0, 7))

    def test_moving_Rook_invalidly_throws_exception(self):
        with self.assertRaises(RookCanOnlyMoveInOneAxisError):
            self.Board.move_white_rook_1(Position(2, 2))

    def test_moving_when_blocked_by_another_piece_throws_exception(self):
        with self.assertRaises(MoveBlockedByPieceError):
            self.Board.move_white_rook_1(Position(0, 4))
            self.Board.move_black_rook_1(Position(0, 2))

    def test_moving_when_not_blocked_by_another_piece_does_not_throw_exception(self):
        self.Board.move_white_rook_1(Position(0, 4))
        self.Board.move_black_rook_1(Position(0, 5))

    def test_get_all_valid_moves(self):
        rook = self.Board.get_white_rook_1()
        moves = rook.get_all_valid_moves(False, self.Board)
        self.assertEqual([
            Position(0, 1),
            Position(0, 2),
            Position(0, 3),
            Position(0, 4),
            Position(0, 5),
            Position(0, 6),
            Position(0, 7)
        ], moves)

    def test_does_square_contain_same_colour_piece_returns_true(self):
        contains_same_colour = self.Board.does_square_contain_same_colour_piece(True, Position(7, 0))
        self.assertEqual(True, contains_same_colour)

    def test_does_square_contain_same_colour_piece_returns_false(self):
        contains_same_colour = self.Board.does_square_contain_same_colour_piece(True, Position(0, 7))
        self.assertEqual(False, contains_same_colour)

    def test_get_white_rook_1(self):
        rook = self.Board.get_white_rook_1()
        self.assertIsInstance(rook, Rook)
        self.assertEqual(1, rook.Id)
        self.assertEqual(True, rook.is_white())

    def test_get_white_knight_1(self):
        knight = self.Board.get_white_knight_1()
        self.assertIsInstance(knight, Knight)
        self.assertEqual(1, knight.Id)
        self.assertEqual(True, knight.is_white())

    def test_get_black_rook_1(self):
        rook = self.Board.get_black_rook_1()
        self.assertIsInstance(rook, Rook)
        self.assertEqual(1, rook.Id)
        self.assertEqual(False, rook.is_white())

    def test_get_white_king(self):
        king = self.Board.get_white_king()
        self.assertIsInstance(king, King)
        self.assertEqual(1, king.Id)
        self.assertEqual(True, king.is_white())

    def test_is_white_king_in_check_returns_false(self):
        new_board = Board(None)
        new_board.move_black_rook_1(Position(0, 5))
        self.assertEqual(False, new_board.is_white_king_in_check())

    def test_is_white_king_in_check_returns_true(self):
        new_board = Board(None)
        new_board.move_black_rook_1(Position(0, 5))
        new_board.move_black_rook_1(Position(4, 5))
        self.assertEqual(True, new_board.is_white_king_in_check())

    def test_would_cause_king_to_be_in_check_throws_exception(self):
        with self.assertRaises(MoveCausesYourKingToBeInCheckError):
            new_board = Board(None)
            new_board.move_white_rook_1(Position(0, 1))
            new_board.move_black_rook_1(Position(0, 6))
            new_board.move_white_rook_1(Position(4, 1))
            new_board.move_black_rook_1(Position(4, 6))
            new_board.move_white_rook_1(Position(5, 1))

    def test_would_cause_king_to_be_in_check_does_not_throw_exception(self):
        new_board = Board(None)
        new_board.move_white_rook_1(Position(0, 1))
        new_board.move_black_rook_1(Position(0, 6))
        new_board.move_white_rook_1(Position(4, 1))
        new_board.move_black_rook_1(Position(4, 6))
        new_board.move_white_rook_1(Position(4, 2))

