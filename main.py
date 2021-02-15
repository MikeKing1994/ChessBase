class Position:
    X: int
    Y: int

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y


def check_move_off_board_error(pos):
    if pos.X not in range(0, 8) or pos.Y not in range(0, 8):
        raise MoveOffBoardError()


def check_move_went_nowhere_error(old_pos, new_pos):
    if new_pos.X == old_pos.X and new_pos.Y == old_pos.Y:
        raise MoveWentNowhereError()


def check_move_blocked_by_other_pieces(b, squares_that_must_be_empty):
    for square in squares_that_must_be_empty:
        if not b.is_square_empty(square):
            raise MoveBlockedByPieceError()


def check_capture_own_piece_error(b, is_white, pos):
    if b.does_square_contain_same_colour_piece(is_white, pos):
        raise CannotCaptureOwnPieceError()


class MoveOffBoardError(Exception):
    def __init__(self):
        self.message = "The given move was off the board x and y values should be between 0 and 8"


class RookCanOnlyMoveInOneAxisError(Exception):
    def __init__(self):
        self.message = "The given move was not valid for a rook, they can only move in one axis"


class BishopMayOnlyMoveDiagonallyError(Exception):
    def __init__(self):
        self.message = "The given move was not valid for a bishop, they can only move diagonally"


class KnightMayOnlyMoveLikeAKnightError(Exception):
    def __init__(self):
        self.message = "The given move was not valid for a knight, they can only move in L shapes"


class MoveBlockedByPieceError(Exception):
    def __init__(self):
        self.message = "The given move would be valid, but there was a piece in the way"


class MoveWentNowhereError(Exception):
    def __init__(self):
        self.message = "The given move didn't go anywhere"


class CannotCaptureOwnPieceError(Exception):
    def __init__(self):
        self.message = "The given move would capture it's own piece"


class Piece:
    IsWhite: bool
    Position: Position
    Taken: bool

    def move_internal(self, pos):
        self.Position = pos

    def taken(self):
        self.Taken = True

    def is_black(self):
        return not self.IsWhite

    def is_white(self):
        return self.IsWhite

    def move(self, b, pos):
        if self.is_move_valid(b, pos):
            print("move was valid, moving to", pos.X, pos.Y)
            self.move_internal(pos)
        else:
            print("move invalid, could not move to", pos.X, pos.Y)

    def is_move_valid(self, b, pos):
        raise Exception("must be implemented by each piece that inherits")

    def get_all_valid_moves(self, b):
        valid_moves = []
        for x in range(0, 8):
            for y in range(0, 8):
                pos = Position(x, y)
                try:
                    if self.is_move_valid(b, pos):
                        valid_moves.append(pos)
                except MoveOffBoardError:
                    print("tried a move, but it wasn't on the board")
                except RookCanOnlyMoveInOneAxisError:
                    print("tried a move, but it wasn't on the same axis for a rook")
                except BishopMayOnlyMoveDiagonallyError:
                    print("tried a move, but it wasn't valid for a bishop")
                except KnightMayOnlyMoveLikeAKnightError:
                    print("tried a move, but it wasn't valid for a knight")
                except MoveBlockedByPieceError:
                    print("tried a move, but it was blocked by a piece")
                except MoveWentNowhereError:
                    print("tried a move, but it went nowhere")
                except CannotCaptureOwnPieceError:
                    print("tried a move, but it would have captured it's own piece")
                finally:
                    pass

        return valid_moves


class Knight(Piece):
    def __init__(self, id, x, y, is_white):
        self.Id = id
        self.Position = Position(x, y)
        self.Taken = False
        self.IsWhite = is_white

    def is_move_valid(self, b, pos):
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

        return True


class Bishop(Piece):
    def __init__(self, id, x, y, is_white):
        self.Id = id
        self.Position = Position(x, y)
        self.Taken = False
        self.IsWhite = is_white

    def is_move_valid(self, b, pos):
        check_move_off_board_error(pos)
        check_move_went_nowhere_error(self.Position, pos)

        delta_x = pos.X - self.Position.X
        delta_y = pos.Y - self.Position.Y

        if abs(delta_x) != abs(delta_y):
            raise BishopMayOnlyMoveDiagonallyError()

        if delta_x > 0 and delta_y > 0:
            squares_that_must_be_empty = [Position(self.Position.X + d, self.Position.Y + d) for d in range(delta_x)]
        if delta_x < 0 and delta_y < 0:
            squares_that_must_be_empty = [Position(self.Position.X - d, self.Position.Y - d) for d in range(delta_x)]
        if delta_x > 0 > delta_y:
            squares_that_must_be_empty = [Position(self.Position.X + d, self.Position.Y - d) for d in range(delta_x)]
        if delta_x < 0 < delta_y:
            squares_that_must_be_empty = [Position(self.Position.X - d, self.Position.Y - d) for d in range(delta_x)]

        check_move_blocked_by_other_pieces(b, squares_that_must_be_empty)
        check_capture_own_piece_error(b, self.is_white(), pos)

        return True


class Rook(Piece):
    def __init__(self, id, x, y, is_white):
        self.Id = id
        self.Position = Position(x, y)
        self.Taken = False
        self.IsWhite = is_white

    def is_move_valid(self, b, pos):
        check_move_off_board_error(pos)
        check_move_went_nowhere_error(self.Position, pos)

        in_same_axis = pos.X == self.Position.X or pos.Y == self.Position.Y
        if not in_same_axis:
            raise RookCanOnlyMoveInOneAxisError()

        step = -1 if (pos.X < self.Position.X or pos.Y < self.Position.Y) else 1

        if step == 1:
            squares_that_must_be_empty_on_x_axis = [Position(axis_val, pos.Y) for axis_val in range(self.Position.X + 1, pos.X, step)]
            squares_that_must_be_empty_on_y_axis = [Position(pos.X, axis_val) for axis_val in range(self.Position.Y + 1, pos.Y, step)]
        elif step == -1:
            squares_that_must_be_empty_on_x_axis = [Position(axis_val, pos.Y) for axis_val in range(self.Position.X - 1, pos.X, step)]
            squares_that_must_be_empty_on_y_axis = [Position(pos.X, axis_val) for axis_val in range(self.Position.Y - 1, pos.Y, step)]

        check_move_blocked_by_other_pieces(b, squares_that_must_be_empty_on_x_axis + squares_that_must_be_empty_on_y_axis)
        check_capture_own_piece_error(b, self.is_white(), pos)

        return True


class Board:
    def __init__(self):
        self.Pieces = [
            Rook(1, 0, 0, True),
            Rook(2, 7, 0, True),
            Rook(1, 0, 7, False),
            Rook(2, 7, 7, False),
            Knight(1, 1, 0, True),
            Knight(2, 6, 0, True),
            Knight(1, 1, 7, False),
            Knight(1, 6, 7, False),
            Bishop(1, 2, 0, True),
            Bishop(2, 5, 0, True),
            Bishop(1, 2, 7, False),
            Bishop(1, 5, 7, False)
        ]

    def get_all_white_pieces(self):
        return [x for x in self.Pieces if x.IsWhite]

    def get_all_black_pieces(self):
        return [x for x in self.Pieces if not x.IsWhite]

    def how_many_pieces_for_white(self):
        pieces = self.get_all_white_pieces()
        return len([x for x in pieces if not x.Taken])

    def how_many_pieces_for_black(self):
        pieces = self.get_all_black_pieces()
        return len([x for x in pieces if not x.Taken])

    def get_white_rook_1(self):
        rook1 = [piece for piece in self.Pieces if piece.is_white() and piece.Id == 1]
        return rook1[0]

    def get_black_rook_1(self):
        rook1 = [piece for piece in self.Pieces if piece.is_black() and piece.Id == 1]
        return rook1[0]

    def move_piece(self, piece_type, is_white, identifier, pos):
        for i, item in enumerate(self.Pieces):
            if isinstance(self.Pieces[i], piece_type):
                if (item.is_white() and is_white) and item.Id == identifier:
                    self.Pieces[i].move(self, pos)
                elif (item.is_black() and (not is_white)) and item.Id == identifier:
                    self.Pieces[i].move(self, pos)

            if (item.is_white() and (not is_white)) and item.Position == pos:
                item.Taken = True
                self.Pieces[i] = item
            if (item.is_black() and is_white) and item.Position == pos:
                item.Taken = True
                self.Pieces[i] = item

    def move_white_rook_1(self, pos):
        self.move_piece(Rook, True, 1, pos)

    def move_black_rook_1(self, pos):
        self.move_piece(Rook, False, 1, pos)

    def is_square_empty(self, pos):
        empty = True
        for item in self.Pieces:
            if item.Position == pos:
                empty = False

        return empty

    def try_get_piece_on_square(self, pos):
        for item in self.Pieces:
            if item.Position == pos:
                return item

        return None

    def does_square_contain_same_colour_piece(self, moving_piece_is_white, pos):
        piece = self.try_get_piece_on_square(pos)
        if piece is None:
            return False
        elif piece.is_white() and moving_piece_is_white:
            return True
        elif piece.is_black() and not moving_piece_is_white:
            return True
        return False

    def print(self):
        for y in range(7, -1, -1):
            rank = []
            for x in range(0, 8):
                if self.is_square_empty(Position(x, y)):
                    rank.append(0)
                else:
                    rank.append(1)

            print(rank)


if __name__ == '__main__':
    board = Board()
    board.print()
    board.move_white_rook_1(Position(0, 4))
    board.print()
    ()


