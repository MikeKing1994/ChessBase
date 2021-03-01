import unittest
from unittest import TestCase

from shared import *
from board import *
from pieces import *


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.Board = Board(None)


class TestInit(TestBoard):
    def test_initial_pieces(self):
        self.assertEqual(32, len(self.Board.Pieces))

    def test_get_all_white_pieces(self):
        all_white = len(self.Board.get_all_white_pieces())
        self.assertEqual(16, all_white)


class TestBoard(TestBoard):
    def test_basic_capture(self):
        new_board = Board(
            [
                Rook(1, 0, 0, True),
                King(1, 4, 0, True),
                Rook(1, 0, 7, False)
            ])
        new_board.move_white_rook_1(Position(0, 7))

        self.assertEqual(False, new_board.get_white_rook_1().Taken)
        self.assertEqual(True, new_board.get_black_rook_1().Taken)

    def test_moving_on_board_does_not_throw_exception(self):
        self.Board.move_white_pawn_1(Position(0, 2))

    def test_moving_off_board_throws_exception(self):
        with self.assertRaises(MoveOffBoardError):
            self.Board.move_white_rook_1(Position(0, 8))

    def test_moving_rook_on_on_one_axis_does_not_throw_exception(self):
        new_board = Board(
            [
                Rook(1, 0, 0, True),
                King(1, 4, 0, True),
                Rook(1, 0, 7, False)
            ])
        new_board.move_white_rook_1(Position(0, 7))

    def test_moving_Rook_invalidly_throws_exception(self):
        with self.assertRaises(RookCanOnlyMoveInOneAxisError):
            self.Board.move_white_rook_1(Position(2, 2))

    def test_moving_when_blocked_by_another_piece_throws_exception(self):
        with self.assertRaises(MoveBlockedByPieceError):
            self.Board.move_white_rook_1(Position(0, 4))
            self.Board.move_black_rook_1(Position(0, 2))

    def test_moving_when_not_blocked_by_another_piece_does_not_throw_exception(self):
        new_board = Board(
            [
                Rook(1, 0, 0, True),
                King(1, 4, 0, True),
                Rook(1, 0, 7, False),
                King(1, 4, 7, False)
            ])
        new_board.move_white_rook_1(Position(0, 4))
        new_board.move_black_rook_1(Position(0, 5))

    def test_get_all_valid_moves(self):
        new_board = Board(
            [
                Rook(1, 0, 0, True),
                Pawn(1, 0, 1, True),
                King(1, 4, 0, True)
            ])
        rook = new_board.get_white_rook_1()
        moves = rook.get_all_valid_moves(False, new_board)
        self.assertEqual([
            Move(Position(0, 0), Position(1, 0)),
            Move(Position(0, 0), Position(2, 0)),
            Move(Position(0, 0), Position(3, 0))
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
        new_board.move_white_pawn_1(Position(0, 2))
        self.assertEqual(False, new_board.is_white_king_in_check())

    def test_is_white_king_in_check_returns_true(self):
        new_board = Board(
            [
                Rook(1, 0, 0, True),
                King(1, 4, 0, True),
                Rook(1, 0, 7, False),
                King(1, 4, 7, False)
            ])
        new_board.move_black_rook_1(Position(0, 5))
        new_board.move_black_rook_1(Position(4, 5))
        self.assertEqual(True, new_board.is_white_king_in_check())

    def test_would_cause_king_to_be_in_check_throws_exception(self):
        with self.assertRaises(MoveCausesYourKingToBeInCheckError):
            new_board = Board(
                [
                    Rook(1, 0, 0, True),
                    King(1, 4, 0, True),
                    Rook(1, 0, 7, False),
                    King(1, 4, 7, False)
                ])
            new_board.move_white_rook_1(Position(0, 1))
            new_board.move_black_rook_1(Position(0, 6))
            new_board.move_white_rook_1(Position(4, 1))
            new_board.move_black_rook_1(Position(4, 6))
            new_board.move_white_rook_1(Position(5, 1))

    def test_would_cause_king_to_be_in_check_does_not_throw_exception(self):
        new_board = Board(
            [
                Rook(1, 4, 1, True),
                King(1, 4, 0, True),
                Rook(1, 4, 6, False),
                King(1, 4, 7, False)
            ])
        new_board.move_white_rook_1(Position(4, 2))

    def test_pawn_can_move_forward_two_from_start(self):
        new_board = Board(None)
        new_board.move_white_pawn_1(Position(0, 3))

    def test_pawn_can_take_diagonally(self):
        new_board = Board([
            Pawn(1, 4, 4, True),
            Pawn(1, 5, 5, False),
            King(1, 4, 0, True)
        ])
        new_board.move_white_pawn_1(Position(5, 5))

    def test_pawn_cant_go_diagonal_if_own_piece_is_there(self):
        with self.assertRaises(CannotCaptureOwnPieceError):
            new_board = Board([
                Pawn(1, 4, 4, True),
                Pawn(1, 5, 5, True),
                King(1, 4, 0, True)
            ])
            new_board.move_white_pawn_1(Position(5, 5))

    def test_pawn_cant_go_diagonal_if_no_piece_is_there(self):
        with self.assertRaises(DiagonalPawnMoveMustBeACaptureError):
            new_board = Board([
                Pawn(1, 4, 4, True),
                King(1, 4, 0, True)
            ])
            new_board.move_white_pawn_1(Position(5, 5))

    def test_get_all_moves_for_white(self):
        pawn = Pawn(1, 0, 1, True)
        king = King(1, 4, 0, True)
        new_board = Board([
            pawn,
            king
        ])
        all_valid_moves = new_board.get_all_moves_for_white()
        expected = [
                Move(Position(0, 1), Position(0, 2)),
                Move(Position(0, 1), Position(0, 3)),
                Move(Position(4, 0), Position(3, 0)),
                Move(Position(4, 0), Position(3, 1)),
                Move(Position(4, 0), Position(4, 1)),
                Move(Position(4, 0), Position(5, 0)),
                Move(Position(4, 0), Position(5, 1))
            ]
        self.assertEqual(expected, all_valid_moves)

    def test_get_all_moves_for_pawn(self):
        pawn = Pawn(1, 0, 1, True)
        king = King(1, 4, 0, True)
        new_board = Board([
            pawn,
            king
        ])
        all_valid_moves = pawn.get_all_valid_moves(False, new_board)
        expected = [
            Move(Position(0, 1), Position(0, 2)),
            Move(Position(0, 1), Position(0, 3))
        ]
        self.assertEqual(expected, all_valid_moves)

    def test_get_all_moves_for_king(self):
        pawn = Pawn(1, 0, 1, True)
        king = King(1, 4, 0, True)
        new_board = Board([
            pawn,
            king
        ])
        all_valid_moves = king.get_all_valid_moves(False, new_board)
        expected = [
            Move(Position(4, 0), Position(3, 0)),
            Move(Position(4, 0), Position(3, 1)),
            Move(Position(4, 0), Position(4, 1)),
            Move(Position(4, 0), Position(5, 0)),
            Move(Position(4, 0), Position(5, 1))
        ]
        self.assertEqual(expected, all_valid_moves)

    def test_piece_equality_returns_true(self):
        a = Rook(1, 1, 1, True)
        b = Rook(1, 1, 1, True)
        self.assertTrue(a == b)

    def test_piece_equality_returns_false(self):
        a = Rook(1, 1, 1, True)
        b = Rook(2, 1, 1, True)
        self.assertFalse(a == b)

    def test_board_equality_returns_true(self):
        pawn_a = Pawn(1, 0, 1, True)
        pawn_b = Pawn(1, 0, 2, True)
        king = King(1, 4, 0, True)
        board_a = Board([
            pawn_a,
            king
        ])
        board_b = Board([
            pawn_a,
            king
        ])
        self.assertTrue(board_a == board_b)

    def test_board_equality_returns_false(self):
        pawn_a = Pawn(1, 0, 1, True)
        pawn_b = Pawn(1, 0, 2, True)
        king = King(1, 4, 0, True)
        board_a = Board([
            pawn_a,
            king
        ])
        board_b = Board([
            pawn_b,
            king
        ])
        self.assertFalse(board_a == board_b)

    # the point of this test is that the pawn on A2 cannot move because of the check
    def test_if_king_is_in_check_then_must_break_check(self):
        pawn = Pawn(1, 0, 1, True)
        king = King(1, 4, 0, True)
        black_bishop = Bishop(1, 5, 1, False)
        new_board = Board([
            pawn,
            king,
            black_bishop
        ])
        self.assertTrue(new_board.is_white_king_in_check())
        all_valid_moves = new_board.get_all_moves_for_white()
        expected = [
            Move(Position(4, 0), Position(3, 0)),
            Move(Position(4, 0), Position(3, 1)),
            Move(Position(4, 0), Position(4, 1)),
            Move(Position(4, 0), Position(5, 0)),
            Move(Position(4, 0), Position(5, 1))
        ]
        self.assertEqual(expected, all_valid_moves)

    def test_king_can_recapture_when_in_check_from_adjacent_piece(self):
        king = King(1, 4, 0, True)
        black_bishop = Bishop(1, 5, 1, False)
        new_board = Board([
            king,
            black_bishop
        ])
        self.assertTrue(new_board.is_white_king_in_check())
        self.assertTrue(king.is_move_valid(False, new_board, Position(5, 1)))

    def test_rook_moving_vertically_down(self):
        with self.assertRaises(MoveBlockedByPieceError):
            rook = Rook(1, 4, 6, False)
            new_board = Board(
                [
                    Rook(1, 4, 1, True),
                    King(1, 4, 0, True),
                    rook,
                    King(1, 4, 7, False)
                ])
            self.assertFalse(rook.is_move_valid(True, new_board, Position(4, 0)))

    def test_pawn_moving_forward_cannot_move_into_a_piece_of_opposite_colour(self):
        with self.assertRaises(MoveBlockedByPieceError):
            pawn = Pawn(1, 2, 2, True)
            new_board = Board(
                [
                    Rook(1, 2, 3, False),
                    King(1, 4, 0, True),
                    pawn,
                    King(1, 4, 7, False)
                ])
            # point being it cannot go there as it would have to capture the rook, which it cannot
            self.assertFalse(pawn.is_move_valid(False, new_board, Position(2, 3)))

    def test_pawn_cannot_move_backwards(self):
        pawn = Pawn(1, 2, 2, True)
        new_board = Board(
            [
                Rook(1, 3, 1, False),
                King(1, 4, 0, True),
                pawn,
                King(1, 4, 7, False)
            ])
        self.assertFalse(pawn.is_move_valid(False, new_board, Position(3, 1)))
