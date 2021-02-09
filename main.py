class Position:
    X: int
    Y: int

    def __init__(self, x, y):
        self.X = x
        self.Y = y


class Piece:
    IsWhite: bool
    Position: Position
    Taken: bool

    def move(self, b, pos):
        self.Position = pos
        self.check_take(b)

    def taken(self):
        self.Taken = True

    def check_take(self, b):
        ()


class Rook(Piece):
    def __init__(self, id, x, y, is_white):
        self.Id = id
        self.Position = Position(x, y)
        self.Taken = False
        self.IsWhite = is_white


class Board:
    def __init__(self):
        self.Pieces = [
            Rook(1, 0, 8, True),
            Rook(2, 8, 0, True),
            Rook(1, 0, 8, False),
            Rook(2, 8, 8, False)
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

    def move_white_rook_1(self, pos):
        for i, item in enumerate(self.Pieces):
            if self.Pieces[i].IsWhite and self.Pieces[i].Id == 1:
                self.Pieces[i].move(self, pos)


if __name__ == '__main__':
    board = Board()
    board.move_white_rook_1(Position(4, 4))
    x = board.get_all_black_pieces()
    print(board.how_many_pieces_for_white())
    print(board.how_many_pieces_for_black())


