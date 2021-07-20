from exceptions import *
import copy


class Position:
    X: int
    Y: int

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    def to_string(self):
        return f'({self.X}, {self.Y})'


class Move:
    From: Position
    To: Position

    def __init__(self, f, to):
        self.From = f
        self.To = to

    def __eq__(self, other):
        return self.From == other.From and self.To == other.To

    def to_string(self):
        return f'{self.From.to_string()} to {self.To.to_string()}'


class Piece:
    Id: int
    IsWhite: bool
    Position: Position
    Taken: bool

    def __eq__(self, other):
        return (other.IsWhite == self.IsWhite) and (other.Position == self.Position) and (other.Id == self.Id) and (other.Taken == self.Taken)

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
            logging.info(f'move was valid, moving to {pos.toString()}')
            self.move_internal(pos)
        else:
            logging.info(f'move invalid, could not move to {pos.toString()}')

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
                except MoveCausesYourKingToBeInCheckError:
                    pass
                    # print("tried a move, but it would have captured it's own piece")
                finally:
                    pass

        return valid_moves


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


def flatten(t): \
        return [item for sublist in t for item in sublist]


def position_to_coordinate(pos):
    return 100 * pos.X, 700 - (100 * pos.Y)
