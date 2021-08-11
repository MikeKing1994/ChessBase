from src.pieces import *
from src.shared import *
import logging
# from PIL import Image, ImageDraw
from typing import Optional


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
                Knight(2, 6, 7, False),
                Bishop(1, 2, 0, True),
                Bishop(2, 5, 0, True),
                Bishop(1, 2, 7, False),
                Bishop(2, 5, 7, False),
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

    def __eq__(self, other):
        all_pieces_have_an_equal = True
        for piece in self.Pieces:
            if piece not in other.Pieces:
                all_pieces_have_an_equal = False

        return all_pieces_have_an_equal

    def copy(self):
        return Board(self.Pieces)

    def get_all_white_pieces(self) -> list[Piece]:
        return [x for x in self.Pieces if x.IsWhite and not x.Taken]

    def get_all_black_pieces(self) -> list[Piece]:
        return [x for x in self.Pieces if not x.IsWhite and not x.Taken]

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

    def try_get_piece_on_square(self, pos: Position) -> Optional[Piece]:
        for item in self.Pieces:
            if item.Position == pos and not item.Taken:
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

    #def pretty_print(self):
    #    im = Image.new('RGB', (900, 900), (128, 128, 128))
    #    draw = ImageDraw.Draw(im)
    #    for y in range(7, -1, -1):
    #        for x in range(0, 8):
    #            is_white = ((x + y) % 2 == 0)
    #            colour = (235, 125, 52) if is_white else (245, 231, 159)
    #            draw.rectangle((100 * x, 100 * y, (100 * x) + 100, (100 * y) + 100), fill=colour,
    #                           outline=(255, 255, 255))
#
#                pos = Position(x, y)
 #               p = self.try_get_piece_on_square(pos)
#
 #               if isinstance(p, King):
  #                  white_king = Image.open('WhiteKing.png').resize((100, 100))
   #                 im.paste(white_king, position_to_coordinate(pos), white_king)
#
 #               if isinstance(p, Queen):
  #                  white_queen = Image.open('WhiteQueen.png').resize((100, 100))
   #                 im.paste(white_queen, position_to_coordinate(pos), white_queen)
#
 #               if isinstance(p, Rook):
  #                  white_rook = Image.open('WhiteRook.png').resize((100, 100))
   #                 im.paste(white_rook, position_to_coordinate(pos), white_rook)
#
 #               if isinstance(p, Bishop):
  #                  white_bishop = Image.open('WhiteBishop.png').resize((100, 100))
   #                 im.paste(white_bishop, position_to_coordinate(pos), white_bishop)
#
 #               if isinstance(p, Knight):
  #                  white_knight = Image.open('WhiteKnight.png').resize((100, 100))
   #                 im.paste(white_knight, position_to_coordinate(pos), white_knight)
#
 #               if isinstance(p, Pawn):
  #                  white_pawn = Image.open('WhitePawn.png').resize((100, 100))
   #                 im.paste(white_pawn, position_to_coordinate(pos), white_pawn)
    #    im.show()

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
            valid_moves_for_white = p.get_all_valid_moves(False, self)
            for move in valid_moves_for_white:
                if move.To == king.Position:
                    return True

        return False

    def get_all_moves_for_white(self) -> list[Move]:
        moves = []
        white_pieces = self.get_all_white_pieces()
        for piece in white_pieces:
            moves.append(piece.get_all_valid_moves(False, self))
        return flatten(moves)

    def get_all_moves_for_black(self) -> list[Move]:
        moves = []
        black_pieces = self.get_all_black_pieces()
        for piece in black_pieces:
            moves.append(piece.get_all_valid_moves(False, self))
        return flatten(moves)

    def is_white_king_checkmated(self):
        if not self.is_white_king_in_check():
            return False
        checkmated = True

        for piece in self.get_all_white_pieces():
            for move in piece.get_all_valid_moves(False, self):
                temp_board = copy.deepcopy(self)
                try:
                    piece.move(temp_board, move.To)
                except:
                    logging.exception("errored checking checkmate")
                if not temp_board.is_white_king_in_check():
                    checkmated = False

        return checkmated

    def is_black_king_checkmated(self):
        if not self.is_black_king_in_check():
            return False
        checkmated = True

        for piece in self.get_all_black_pieces():
            for move in piece.get_all_valid_moves(False, self):
                temp_board = copy.deepcopy(self)
                try:
                    piece.move(temp_board, move.To)
                except:
                    logging.exception("errored checking checkmate")
                if not temp_board.is_black_king_in_check():
                    checkmated = False

        return checkmated
