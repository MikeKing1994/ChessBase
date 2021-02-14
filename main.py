class Position:
    X: int
    Y: int

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y


class MoveOffBoardError(Exception):
    def __init__(self):
        self.message = "The given move was off the board x and y values should be between 0 and 8"


class RookCanOnlyMoveInOneAxisError(Exception):
    def __init__(self):
        self.message = "The given move was not valid for a rook, they can only move in one axis"


class MoveBlockedByPieceError(Exception):
    def __init__(self):
        self.message = "The given move would be valid, but there was a piece in the way"


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


class Rook(Piece):
    def __init__(self, id, x, y, is_white):
        self.Id = id
        self.Position = Position(x, y)
        self.Taken = False
        self.IsWhite = is_white

    def is_move_valid(self, b, pos):
        if pos.X not in range(0, 8) or pos.Y not in range(0, 8):
            raise MoveOffBoardError()
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

        for square in squares_that_must_be_empty_on_x_axis + squares_that_must_be_empty_on_y_axis:
            if not b.is_square_empty(square):
                raise MoveBlockedByPieceError()

        return pos.X == self.Position.X or pos.Y == self.Position.Y

    def move(self, b, pos):
        if self.is_move_valid(b, pos):
            print("move was valid, moving to", pos.X, pos.Y)
            self.move_internal(pos)
        else:
            print("move invalid, could not move to", pos.X, pos.Y)


class Board:
    def __init__(self):
        self.Pieces = [
            Rook(1, 0, 0, True),
            Rook(2, 7, 0, True),
            Rook(1, 0, 7, False),
            Rook(2, 7, 7, False)
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

    def move_piece(self, is_white, identifier, pos):
        for i, item in enumerate(self.Pieces):
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
        self.move_piece(True, 1, pos)

    def move_black_rook_1(self, pos):
        self.move_piece(False, 1, pos)

    def is_square_empty(self, pos):
        empty = True
        for item in self.Pieces:
            if item.Position == pos:
                empty = False

        return empty


if __name__ == '__main__':
    board = Board()
    board.move_white_rook_1(Position(0, 4))
    ()


