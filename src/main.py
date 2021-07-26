from exceptions import *

import asyncio
from puppeteer import start_game_against_jimmy_on_chess_dot_com, move_piece_on_chess_dot_com, read_board, \
    get_board_only_after_opponent_plays, is_game_over
from shared import *
from pieces import King, Queen, Bishop, Knight, Rook, Pawn
from board import Board
import time
import random
from file_logging import set_up_log_file
import logging
import sys


def log_unhandled_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = log_unhandled_exception


class RandomGameBot:
    board: Board

    def __init__(self):
        board = Board()

    def play_cycle(self, game_driver):
        self.board = read_board(game_driver)
        all_valid_moves = self.board.get_all_moves_for_white()

        if all_valid_moves:
            first_move = random.choice(all_valid_moves)
            logging.info('Attempting move: %s', first_move.to_string())

            try:
                move_piece_on_chess_dot_com(game_driver, first_move.From, first_move.To)
            except ChessDotComThinksGameIsOver:
                logging.exception("exception thrown")
                return True

        updated_board = get_board_only_after_opponent_plays(game_driver, self.board)

        if updated_board.is_white_king_checkmated() or updated_board.is_black_king_checkmated():
            self.board = updated_board
            return True

        return False

    def play(self):
        set_up_log_file()
        logging.info('Game started')

        game_driver = start_game_against_jimmy_on_chess_dot_com()
        self.board = read_board(game_driver)
        game_over = False

        while not game_over:
            game_over = self.play_cycle(game_driver)

        logging.info('Game complete')

        if self.board.is_white_king_checkmated():
            logging.info("we lost :-(")
        else:
            logging.info("we actually won!!!")


class SelfPlay:
    def __init__(self):
        self.board = Board()

    def white_play_cycle(self):
        all_valid_moves = self.board.get_all_moves_for_white()
        if all_valid_moves:
            first_move = random.choice(all_valid_moves)
            piece_to_move = self.board.try_get_piece_on_square(first_move.From)

            logging.info('Attempting white move: %s', first_move.to_string())

            if piece_to_move is not None:
                type_of_piece = type(piece_to_move)
                self.board.move_piece(type_of_piece, piece_to_move.IsWhite, piece_to_move.Id, first_move.To)

        if self.board.is_white_king_checkmated() or self.board.is_black_king_checkmated():
            return True

        return False

    def black_play_cycle(self):
        all_valid_moves = self.board.get_all_moves_for_black()
        if all_valid_moves:
            first_move = random.choice(all_valid_moves)
            piece_to_move = self.board.try_get_piece_on_square(first_move.From)

            logging.info('Attempting black move: %s', first_move.to_string())

            if piece_to_move is not None:
                type_of_piece = type(piece_to_move)
                self.board.move_piece(type_of_piece, piece_to_move.IsWhite, piece_to_move.Id, first_move.To)

        if self.board.is_white_king_checkmated() or self.board.is_black_king_checkmated():
            return True

        return False


def play_against_self():
    set_up_log_file()
    logging.info('Game started')

    bot = SelfPlay()

    game_over = False
    whites_move = True

    while not game_over:
        if whites_move:
            game_over = bot.white_play_cycle()
            whites_move = not whites_move
            bot.board.print()
        else:
            game_over = bot.black_play_cycle()
            whites_move = not whites_move
            bot.board.print()

    logging.info('Game complete')

    if bot.board.is_white_king_checkmated():
        logging.info("white lost :-(")
    else:
        logging.info("black lost!!!")


if __name__ == '__main__':
    play_against_self()

    ()
