from shared import *
from exceptions import *


class Knight(Piece):
    def __init__(self, id, x, y, is_white):
        self.Id = id
        self.Position = Position(x, y)
        self.Taken = False
        self.IsWhite = is_white

    def is_move_valid(self, ignore_king_check, b, pos):
        check_move_off_board_error(pos)
        check_move_went_nowhere_error(self.Position, pos)
        check_capture_own_piece_error(b, self.is_white(), pos)

        delta_x = pos.X - self.Position.X
        delta_y = pos.Y - self.Position.Y

        move_valid = False

        if abs(delta_x) == 2 and abs(delta_y == 1):
            move_valid = True
        elif abs(delta_x) == 1 and abs(delta_y) == 2:
            move_valid = True

        if not move_valid:
            raise KnightMayOnlyMoveLikeAKnightError()

        if not ignore_king_check:
            check_causes_king_to_be_in_check_error(b, self.IsWhite, Knight, self.Id, pos)

        return True


class Queen(Piece):
    def __init__(self, id, x, y, is_white):
        self.Id = id
        self.Position = Position(x, y)
        self.Taken = False
        self.IsWhite = is_white

    def is_move_valid(self, ignore_king_check, b, pos):
        check_move_off_board_error(pos)
        check_move_went_nowhere_error(self.Position, pos)
        check_capture_own_piece_error(b, self.is_white(), pos)

        delta_x = pos.X - self.Position.X
        delta_y = pos.Y - self.Position.Y

        move_valid = False

        if delta_x == 0 or delta_y == 0:
            move_valid = True
        elif abs(delta_x) == abs(delta_y):
            move_valid = True
        if not move_valid:
            raise QueenMayOnlyMoveLikeAQueenError()

        if delta_x > 0 and delta_y > 0:  # diagonally up right
            squares_that_must_be_empty = [Position(self.Position.X + d, self.Position.Y + d) for d in range(1, abs(delta_x))]
        if delta_x < 0 and delta_y < 0:  # diagonally left down
            squares_that_must_be_empty = [Position(self.Position.X - d, self.Position.Y - d) for d in range(1, abs(delta_x))]
        if delta_x > 0 > delta_y:  # diagonally down right
            squares_that_must_be_empty = [Position(self.Position.X + d, self.Position.Y - d) for d in range(1, abs(delta_x))]
        if delta_x < 0 < delta_y:  # diagonally down left
            squares_that_must_be_empty = [Position(self.Position.X - d, self.Position.Y + d) for d in range(1, abs(delta_x))]
        if delta_x == 0 and delta_y > 0:  # vertically up
            squares_that_must_be_empty = [Position(pos.X, axis_val) for axis_val in
                                          range(self.Position.Y + 1, pos.Y, 1)]
        if delta_x == 0 and delta_y < 0:  # vertically down
            squares_that_must_be_empty = [Position(pos.X, axis_val) for axis_val in
                                          range(self.Position.Y - 1, pos.Y, -1)]
        if delta_y == 0 and delta_x < 0:  # horizontally left
            squares_that_must_be_empty = [Position(axis_val, pos.Y) for axis_val in
                                          range(self.Position.X - 1, pos.X, -1)]
        if delta_y == 0 and delta_x > 0:  # horizontally right
            squares_that_must_be_empty = [Position(axis_val, pos.Y) for axis_val in
                                          range(self.Position.X + 1, pos.X, 1)]

        check_move_blocked_by_other_pieces(b, squares_that_must_be_empty)
        if not ignore_king_check:
            check_causes_king_to_be_in_check_error(b, self.IsWhite, Queen, self.Id, pos)

        return True


class King(Piece):
    def __init__(self, id, x, y, is_white):
        self.Id = id
        self.Position = Position(x, y)
        self.Taken = False
        self.IsWhite = is_white

    def is_move_valid(self, ignore_king_check, b, pos):
        check_move_off_board_error(pos)
        check_move_went_nowhere_error(self.Position, pos)
        check_capture_own_piece_error(b, self.is_white(), pos)

        delta_x = pos.X - self.Position.X
        delta_y = pos.Y - self.Position.Y

        move_valid = False

        if (abs(delta_x) in [1, 0]) and (abs(delta_y) in [1, 0]):
            # no need for a check here, because if the square has our own piece on it then we have already tested for this
            move_valid = True
        if not move_valid:
            raise KingMayOnlyMoveLikeAKingError()
        if not ignore_king_check:
            check_causes_king_to_be_in_check_error(b, self.IsWhite, King, self.Id, pos)

        return True


class Pawn(Piece):
    def __init__(self, id, x, y, is_white):
        self.Id = id
        self.Position = Position(x, y)
        self.Taken = False
        self.IsWhite = is_white

    def is_move_valid(self, ignore_king_check, b, pos):
        check_move_off_board_error(pos)
        check_move_went_nowhere_error(self.Position, pos)
        check_capture_own_piece_error(b, self.is_white(), pos)

        delta_x = pos.X - self.Position.X
        delta_y = pos.Y - self.Position.Y

        move_valid = False

        # Normal move directly forward for white
        if self.IsWhite and delta_y == 1 and delta_x == 0:
            check_move_blocked_by_other_pieces(b, [pos])
            move_valid = True

        # Normal move directly down for black
        if (not self.IsWhite) and delta_y == -1 and delta_x == 0:
            check_move_blocked_by_other_pieces(b, [pos])
            move_valid = True

        # capture diagonally, must be a capture
        if abs(delta_y) == 1 and abs(delta_x) == 1:
            piece_on_new_square = b.try_get_piece_on_square(pos)
            if piece_on_new_square is None or (piece_on_new_square.is_white() == self.IsWhite):
                raise DiagonalPawnMoveMustBeACaptureError()
            move_valid = True

        # Can move two squares forward from it's starting position for white
        if self.IsWhite and delta_y == 2 and delta_x == 0 and self.Position.Y == 1:
            check_move_blocked_by_other_pieces(b, [
                Position(self.Position.X, self.Position.Y + 1),
                Position(self.Position.X, self.Position.Y + 2)])
            move_valid = True

        # Can move two squares forward from it's starting position for black
        if (not self.IsWhite) and delta_y == -2 and delta_x == 0 and self.Position.Y == 6:
            check_move_blocked_by_other_pieces(b, [
                Position(self.Position.X, self.Position.Y - 1),
                Position(self.Position.X, self.Position.Y - 2)])
            move_valid = True

        if not move_valid:
            raise PawnMayOnlyMoveLikeAPawnError()

        if not ignore_king_check:
            check_causes_king_to_be_in_check_error(b, self.IsWhite, Pawn, self.Id, pos)

        return True


class Bishop(Piece):
    def __init__(self, id, x, y, is_white):
        self.Id = id
        self.Position = Position(x, y)
        self.Taken = False
        self.IsWhite = is_white

    def is_move_valid(self, ignore_king_check, b, pos):
        check_move_off_board_error(pos)
        check_move_went_nowhere_error(self.Position, pos)

        delta_x = pos.X - self.Position.X
        delta_y = pos.Y - self.Position.Y

        if abs(delta_x) != abs(delta_y):
            raise BishopMayOnlyMoveDiagonallyError()

        if delta_x > 0 and delta_y > 0:
            squares_that_must_be_empty = [Position(self.Position.X + d, self.Position.Y + d) for d in range(1, abs(delta_x))]
        if delta_x < 0 and delta_y < 0:
            squares_that_must_be_empty = [Position(self.Position.X - d, self.Position.Y - d) for d in range(1, abs(delta_x))]
        if delta_x > 0 > delta_y:
            squares_that_must_be_empty = [Position(self.Position.X + d, self.Position.Y - d) for d in range(1, abs(delta_x))]
        if delta_x < 0 < delta_y:
            squares_that_must_be_empty = [Position(self.Position.X - d, self.Position.Y + d) for d in range(1, abs(delta_x))]

        check_move_blocked_by_other_pieces(b, squares_that_must_be_empty)
        check_capture_own_piece_error(b, self.is_white(), pos)
        if not ignore_king_check:
            check_causes_king_to_be_in_check_error(b, self.IsWhite, Bishop, self.Id, pos)

        return True


class Rook(Piece):
    def __init__(self, id, x, y, is_white):
        self.Id = id
        self.Position = Position(x, y)
        self.Taken = False
        self.IsWhite = is_white

    def is_move_valid(self, ignore_king_check, b, pos):
        check_move_off_board_error(pos)
        check_move_went_nowhere_error(self.Position, pos)

        in_same_axis = pos.X == self.Position.X or pos.Y == self.Position.Y
        if not in_same_axis:
            raise RookCanOnlyMoveInOneAxisError()

        delta_x = pos.X - self.Position.X
        delta_y = pos.Y - self.Position.Y

        if delta_x == 0 and delta_y > 0:  # vertically up
            squares_that_must_be_empty = [Position(pos.X, axis_val) for axis_val in
                                          range(self.Position.Y + 1, pos.Y, 1)]
        if delta_x == 0 and delta_y < 0:  # vertically down
            squares_that_must_be_empty = [Position(pos.X, axis_val) for axis_val in
                                          range(self.Position.Y - 1, pos.Y, -1)]
        if delta_y == 0 and delta_x < 0:  # horizontally left
            squares_that_must_be_empty = [Position(axis_val, pos.Y) for axis_val in
                                          range(self.Position.X - 1, pos.X, -1)]
        if delta_y == 0 and delta_x > 0:  # horizontally right
            squares_that_must_be_empty = [Position(axis_val, pos.Y) for axis_val in
                                          range(self.Position.X + 1, pos.X, 1)]

        check_move_blocked_by_other_pieces(b, squares_that_must_be_empty)
        check_capture_own_piece_error(b, self.is_white(), pos)
        if not ignore_king_check:
            check_causes_king_to_be_in_check_error(b, self.IsWhite, Rook, self.Id, pos)

        return True