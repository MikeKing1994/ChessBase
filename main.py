from exceptions import *

import asyncio
from puppeteer import start_game_against_jimmy_on_chess_dot_com, move_piece_on_chess_dot_com, read_board, \
    get_board_only_after_opponent_plays
from shared import *
from pieces import King, Queen, Bishop, Knight, Rook, Pawn
from board import Board
import time
import random


class RandomGameBot:
    board: Board

    def __init__(self):
        board = Board()

    def play_cycle(self, game_driver):
        self.board = read_board(game_driver)
        all_valid_moves = self.board.get_all_moves_for_white()
        if all_valid_moves:
            first_move = random.choice(all_valid_moves)
            move_piece_on_chess_dot_com(game_driver, first_move.From, first_move.To)
        get_board_only_after_opponent_plays(game_driver, self.board)

    def play(self):
        game_driver = start_game_against_jimmy_on_chess_dot_com()
        self.board = read_board(game_driver)
        for i in range(100):
            self.play_cycle(game_driver)


if __name__ == '__main__':
    random_bot = RandomGameBot()
    random_bot.play()
    ()
