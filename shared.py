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

