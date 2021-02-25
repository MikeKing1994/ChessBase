from exceptions import *
import copy
from PIL import Image, ImageDraw


def position_to_coordinate(pos):
    return 100 * pos.X, 700 - (100 * pos.Y)


def flatten(t): \
    return [item for sublist in t for item in sublist]


class Position:
    X: int
    Y: int

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y


class Move:
    From: Position
    To: Position

    def __init__(self, f, to):
        self.From = f
        self.To = to

    def __eq__(self, other):
        return self.From == other.From and self.To == other.To


def check_move_off_board_error(pos):
    if pos.X not in range(0, 8) or pos.Y not in range(0, 8):
        raise MoveOffBoardError()


def check_move_went_nowhere_error(old_pos, new_pos):
    if new_pos.X == old_pos.X and new_pos.Y == old_pos.Y:
        raise MoveWentNowhereError()


def check_move_blocked_by_other_pieces(b, squares_that_must_be_empty):
    for square in squares_that_must_be_empty:
        # hack this needs to check if the piece on the square is the same colour
        if not b.is_square_empty(square):
            raise MoveBlockedByPieceError()


def check_capture_own_piece_error(b, is_white, pos):
    if b.does_square_contain_same_colour_piece(is_white, pos):
        raise CannotCaptureOwnPieceError()


def check_causes_king_to_be_in_check_error(b, is_white, piece_type, identifier, pos):
    temp_board = copy.deepcopy(b)
    temp_board.dangerously_move_piece_with_no_validity_checks(piece_type, is_white, identifier, pos)
    if is_white and temp_board.is_white_king_in_check():
        raise MoveCausesYourKingToBeInCheckError()
    elif not is_white and temp_board.is_black_king_in_check():
        raise MoveCausesYourKingToBeInCheckError()


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
        if self.is_move_valid(False, b, pos):
            print("move was valid, moving to", pos.X, pos.Y)
            self.move_internal(pos)
        else:
            print("move invalid, could not move to", pos.X, pos.Y)

    # hack should not use this inheritance trick, should define an interface
    def is_move_valid(self, ignore_king_check, b, pos):
        raise Exception("must be implemented by each piece that inherits")

    def get_all_valid_moves(self, ignore_king_check, b):
        valid_moves = []
        for x in range(0, 8):
            for y in range(0, 8):
                pos = Position(x, y)
                try:
                    if self.is_move_valid(ignore_king_check, b, pos):
                        valid_moves.append(Move(self.Position, pos))
                except MoveOffBoardError:
                    pass
                    # print("tried a move, but it wasn't on the board")
                except RookCanOnlyMoveInOneAxisError:
                    pass
                    # print("tried a move, but it wasn't on the same axis for a rook")
                except BishopMayOnlyMoveDiagonallyError:
                    pass
                    # print("tried a move, but it wasn't valid for a bishop")
                except KnightMayOnlyMoveLikeAKnightError:
                    pass
                    # print("tried a move, but it wasn't valid for a knight")
                except QueenMayOnlyMoveLikeAQueenError:
                    pass
                    # print("tried a move, but it wasn't valid for a knight")
                except KingMayOnlyMoveLikeAKingError:
                    pass
                    # print("tried a move, but it wasn't valid for a knight")
                except PawnMayOnlyMoveLikeAPawnError:
                    pass
                    # print("tried a move, but it wasn't valid for a pawn")
                except DiagonalPawnMoveMustBeACaptureError:
                    pass
                    # print("tried a move, but it wasn't valid for a pawn")
                except MoveBlockedByPieceError:
                    pass
                    # print("tried a move, but it was blocked by a piece")
                except MoveWentNowhereError:
                    pass
                    # print("tried a move, but it went nowhere")
                except CannotCaptureOwnPieceError:
                    pass
                    # print("tried a move, but it would have captured it's own piece")
                finally:
                    pass

        return valid_moves


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
            squares_that_must_be_empty = [Position(self.Position.X + d, self.Position.Y + d) for d in range(delta_x)]
        if delta_x < 0 and delta_y < 0:  # diagonally left down
            squares_that_must_be_empty = [Position(self.Position.X - d, self.Position.Y - d) for d in range(delta_x)]
        if delta_x > 0 > delta_y:  # diagonally down right
            squares_that_must_be_empty = [Position(self.Position.X + d, self.Position.Y - d) for d in range(delta_x)]
        if delta_x < 0 < delta_y:  # diagonally down left
            squares_that_must_be_empty = [Position(self.Position.X - d, self.Position.Y - d) for d in range(delta_x)]
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
            check_move_blocked_by_other_pieces(b, [pos])
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
            squares_that_must_be_empty = [Position(self.Position.X + d, self.Position.Y + d) for d in range(delta_x)]
        if delta_x < 0 and delta_y < 0:
            squares_that_must_be_empty = [Position(self.Position.X - d, self.Position.Y - d) for d in range(delta_x)]
        if delta_x > 0 > delta_y:
            squares_that_must_be_empty = [Position(self.Position.X + d, self.Position.Y - d) for d in range(delta_x)]
        if delta_x < 0 < delta_y:
            squares_that_must_be_empty = [Position(self.Position.X - d, self.Position.Y - d) for d in range(delta_x)]

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


class Board:
    def __init__(self, pieces = None):
        if pieces is None:
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
                Bishop(1, 5, 7, False),
                Queen(1, 3, 0, True),
                Queen(1, 3, 7, False),
                King(1, 4, 0, True),
                King(1, 4, 7, False),
                Pawn(1, 0, 1, True),
                Pawn(2, 1, 1, True),
                Pawn(3, 2, 1, True),
                Pawn(4, 3, 1, True),
                Pawn(5, 4, 1, True),
                Pawn(6, 5, 1, True),
                Pawn(7, 6, 1, True),
                Pawn(8, 7, 1, True),
                Pawn(1, 0, 6, False),
                Pawn(2, 1, 6, False),
                Pawn(3, 2, 6, False),
                Pawn(4, 3, 6, False),
                Pawn(5, 4, 6, False),
                Pawn(6, 5, 6, False),
                Pawn(7, 6, 6, False),
                Pawn(8, 7, 6, False)
            ]
        else:
            self.Pieces = pieces

    def copy(self):
        return Board(self.Pieces)

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
        return next((piece for piece in self.Pieces if piece.is_white() and piece.Id == 1 and isinstance(piece, Rook)))

    def get_white_knight_1(self):
        return next((piece for piece in self.Pieces if piece.is_white() and piece.Id == 1 and isinstance(piece, Knight)))

    def get_white_king(self):
        return next((piece for piece in self.Pieces if piece.is_white() and piece.Id == 1 and isinstance(piece, King)))

    def get_black_king(self):
        return next((piece for piece in self.Pieces if piece.is_black() and piece.Id == 1 and isinstance(piece, King)))

    def get_black_rook_1(self):
        return next((piece for piece in self.Pieces if piece.is_black() and piece.Id == 1 and isinstance(piece, Rook)))

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

    def dangerously_move_piece_with_no_validity_checks(self, piece_type, is_white, identifier, pos):
        for i, item in enumerate(self.Pieces):
            if isinstance(self.Pieces[i], piece_type):
                if (item.is_white() and is_white) and item.Id == identifier:
                    item.Position = pos
                elif (item.is_black() and (not is_white)) and item.Id == identifier:
                    item.Position = pos

            if (item.is_white() and (not is_white)) and item.Position == pos:
                item.Taken = True
                self.Pieces[i] = item
            if (item.is_black() and is_white) and item.Position == pos:
                item.Taken = True
                self.Pieces[i] = item

    def move_white_rook_1(self, pos):
        self.move_piece(Rook, True, 1, pos)

    def move_white_pawn_1(self, pos):
        self.move_piece(Pawn, True, 1, pos)

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
                piece_on_square = self.try_get_piece_on_square(Position(x, y))
                if isinstance(piece_on_square, King):
                    rank.append('K')
                elif isinstance(piece_on_square, Queen):
                    rank.append('Q')
                elif isinstance(piece_on_square, Knight):
                    rank.append('N')
                elif isinstance(piece_on_square, Bishop):
                    rank.append('B')
                elif isinstance(piece_on_square, Rook):
                    rank.append('R')
                elif isinstance(piece_on_square, Pawn):
                    rank.append('P')

                else:
                    rank.append('0')

            print(rank)

    def pretty_print(self):
        im = Image.new('RGB', (900, 900), (128, 128, 128))
        draw = ImageDraw.Draw(im)
        for y in range(7, -1, -1):
            for x in range(0, 8):
                is_white = ((x + y) % 2 == 0)
                colour = (235, 125, 52) if is_white else (245, 231, 159)
                draw.rectangle((100 * x, 100 * y, (100 * x) + 100, (100 * y) + 100), fill=colour,
                               outline=(255, 255, 255))

                pos = Position(x, y)
                p = self.try_get_piece_on_square(pos)

                if isinstance(p, King):
                    white_king = Image.open('WhiteKing.png').resize((100, 100))
                    im.paste(white_king, position_to_coordinate(pos), white_king)

                if isinstance(p, Queen):
                    white_queen = Image.open('WhiteQueen.png').resize((100, 100))
                    im.paste(white_queen, position_to_coordinate(pos), white_queen)

                if isinstance(p, Rook):
                    white_rook = Image.open('WhiteRook.png').resize((100, 100))
                    im.paste(white_rook, position_to_coordinate(pos), white_rook)

                if isinstance(p, Bishop):
                    white_bishop = Image.open('WhiteBishop.png').resize((100, 100))
                    im.paste(white_bishop, position_to_coordinate(pos), white_bishop)

                if isinstance(p, Knight):
                    white_knight = Image.open('WhiteKnight.png').resize((100, 100))
                    im.paste(white_knight, position_to_coordinate(pos), white_knight)

                if isinstance(p, Pawn):
                    white_pawn = Image.open('WhitePawn.png').resize((100, 100))
                    im.paste(white_pawn, position_to_coordinate(pos), white_pawn)
        im.show()

    def is_white_king_in_check(self):
        black_pieces = self.get_all_black_pieces()
        king = self.get_white_king()
        for p in black_pieces:
            valid_moves_for_black = p.get_all_valid_moves(True, self)
            for move in valid_moves_for_black:
                if move.To == king.Position:
                    return True

        return False

    def is_black_king_in_check(self):
        white_pieces = self.get_all_white_pieces()
        king = self.get_black_king()
        for p in white_pieces:
            valid_moves_for_white = p.get_all_valid_moves(True, self)
            for move in valid_moves_for_white:
                if move.To == king.Position:
                    return True

        return False

    def get_all_moves_for_white(self):
        moves = []
        white_pieces = self.get_all_white_pieces()
        for piece in white_pieces:
            moves.append(piece.get_all_valid_moves(False, self))
        return flatten(moves)

    def is_white_king_checkmated(self):
        if not self.is_white_king_in_check():
            return False
        # not finished


if __name__ == '__main__':
    board = Board(None)
    board.move_white_pawn_1(Position(0, 3))
    board.pretty_print()

    ()
