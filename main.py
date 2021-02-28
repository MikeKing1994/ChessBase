from exceptions import *

import asyncio
from puppeteer import start_game_against_jimmy_on_chess_dot_com, move_piece_on_chess_dot_com
from shared import *
from pieces import King, Queen, Bishop, Knight, Rook, Pawn
from board import Board


class RandomGameBot:
    def __init__(self):
        board = Board()


if __name__ == '__main__':
    driver = start_game_against_jimmy_on_chess_dot_com()
    move_piece_on_chess_dot_com(driver, Position(3, 1), Position(3, 3))
    move_piece_on_chess_dot_com(driver, Position(4, 1), Position(4, 3))
    ()
