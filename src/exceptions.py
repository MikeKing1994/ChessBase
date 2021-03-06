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


class QueenMayOnlyMoveLikeAQueenError(Exception):
    def __init__(self):
        self.message = \
            "The given move was not valid for a queen, they can only move diagonally, vertically or horizontally"


class KingMayOnlyMoveLikeAKingError(Exception):
    def __init__(self):
        self.message = \
            "The given move was not valid for a king, they can only move one square"


class MoveCausesYourKingToBeInCheckError(Exception):
    def __init__(self):
        self.message = \
            "The given move would cause your king to be in check."


class PawnMayOnlyMoveLikeAPawnError(Exception):
    def __init__(self):
        self.message = \
            "The given move was not valid for a pawn, they can only move forward or diag one square."


class DiagonalPawnMoveMustBeACaptureError(Exception):
    def __init__(self):
        self.message = \
            "The given move was not valid for a pawn, they can only move forward or diag one square."


class MoveBlockedByPieceError(Exception):
    def __init__(self):
        self.message = "The given move would be valid, but there was a piece in the way"


class MoveWentNowhereError(Exception):
    def __init__(self):
        self.message = "The given move didn't go anywhere"


class CannotCaptureOwnPieceError(Exception):
    def __init__(self):
        self.message = "The given move would capture it's own piece"


class ChessDotComWillNotAllowMove(Exception):
    def __init__(self, from_position, to_position):
        self.message = f"we tried to move from: {from_position} to {to_position}, but chess.com wouldn't allow it"


class ChessDotComThinksGameIsOver(Exception):
    def __init__(self, from_position, to_position):
        self.message = f"we tried to move from: {from_position} to {to_position}, but chess.com has the game over overlay open"
