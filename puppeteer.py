from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from shared import Position
from pieces import King, Queen, Bishop, Knight, Rook, Pawn
from board import Board
from exceptions import ChessDotComWillNotAllowMove, ChessDotComThinksGameIsOver
import time


def get_chess_dot_com_square_name_from_position(pos):
    x = str(pos.X + 1)
    y = str(pos.Y + 1)
    return f'square-{x}{y}'


def read_element_by_class_name(driver, target_class_name, must_contain_class):
    elements = driver.find_elements_by_class_name(target_class_name)
    if not elements:
        return None
    else:
        located_class_names = []
        for dom_element in elements:
            try:
                located_class_names.append((dom_element, dom_element.get_attribute("class")))
            except StaleElementReferenceException:
                pass

        if not located_class_names:
            print("couldn't find it, going back around")
            read_element_by_class_name(driver, target_class_name, must_contain_class)

        if must_contain_class is None:
            return located_class_names[0][0]
        else:
            for (dom, class_name) in located_class_names:
                if must_contain_class in class_name:
                    return dom

        return None


def _move_piece_internal(driver, action_chains, move_from_class, move_to_class):
    if is_game_over(driver):
        raise ChessDotComThinksGameIsOver()

    move_from = read_element_by_class_name(driver, move_from_class, "piece")
    if move_from is None:
        raise ChessDotComWillNotAllowMove(move_from_class, move_to_class)
    move_from.click()

    move_to = read_element_by_class_name(driver, move_to_class, "hint")
    if move_to is None:
        raise ChessDotComWillNotAllowMove(move_from_class, move_to_class)

    action_chains.drag_and_drop(move_from, move_to).perform()


def move_piece_on_chess_dot_com(driver, from_position, to_position):
    action_chains = ActionChains(driver)

    from_class = get_chess_dot_com_square_name_from_position(from_position)
    to_class = get_chess_dot_com_square_name_from_position(to_position)

    _move_piece_internal(driver, action_chains, from_class, to_class)


def wait_until_board_loaded(wait):
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "square-42"))
    )


def read_class_of_square(driver, pos, must_contain_class):
    square_class_name = get_chess_dot_com_square_name_from_position(pos)
    element = read_element_by_class_name(driver, square_class_name, must_contain_class)
    if element is not None:
        return element.get_attribute("class")

    return None


def read_piece_on_square(driver, pos):
    class_on_square = read_class_of_square(driver, pos, "piece")
    if class_on_square is None:
        return None
    else:
        if "wr" in class_on_square:
            return Rook(1, pos.X, pos.Y, True) # hack autoset the id to 1
        if "wn" in class_on_square:
            return Knight(1, pos.X, pos.Y, True) # hack autoset the id to 1
        if "wb" in class_on_square:
            return Bishop(1, pos.X, pos.Y, True) # hack autoset the id to 1
        if "wq" in class_on_square:
            return Queen(1, pos.X, pos.Y, True) # hack autoset the id to 1
        if "wk" in class_on_square:
            return King(1, pos.X, pos.Y, True) # hack autoset the id to 1
        if "wp" in class_on_square:
            return Pawn(1, pos.X, pos.Y, True) # hack autoset the id to 1
        if "br" in class_on_square:
            return Rook(1, pos.X, pos.Y, False) # hack autoset the id to 1
        if "bn" in class_on_square:
            return Knight(1, pos.X, pos.Y, False) # hack autoset the id to 1
        if "bb" in class_on_square:
            return Bishop(1, pos.X, pos.Y, False) # hack autoset the id to 1
        if "bq" in class_on_square:
            return Queen(1, pos.X, pos.Y, False) # hack autoset the id to 1
        if "bk" in class_on_square:
            return King(1, pos.X, pos.Y, False) # hack autoset the id to 1
        if "bp" in class_on_square:
            return Pawn(1, pos.X, pos.Y, False) # hack autoset the id to 1


def read_board(driver):
    board_accumulator = Board([])
    # maybe add a check here that the number of taken pieces, plus the number of pieces found should be 32
    for x in range(8):
        for y in range(8):
            pos = Position(x, y)
            piece = read_piece_on_square(driver, pos)
            if piece is not None:
                board_accumulator.Pieces.append(piece)

    return board_accumulator


def get_board_only_after_opponent_plays(driver, previous_board):
    keep_checking = True
    while keep_checking:
        time.sleep(2)
        current_board = read_board(driver)
        if not current_board == previous_board:
            keep_checking = False

    return current_board


def start_game_against_jimmy_on_chess_dot_com():
    driver = webdriver.Firefox(executable_path=r'geckodriver\geckodriver.exe')
    driver.get("https://www.chess.com/play/computer")
    wait = WebDriverWait(driver, 10)

    try:
        annoying_overlay = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "modal-seo-close-icon"))
        )
        annoying_overlay.click()
    except:
        driver.quit()

    choose_button = driver.find_element_by_css_selector("div.selection-menu-footer button")
    choose_button.click()

    play_button = driver.find_element_by_css_selector("div.selection-menu-footer button")
    play_button.click()

    wait_until_board_loaded(wait)

    print("game started")
    return driver


def is_game_over(driver):
    read_element_by_class_name(driver, "modal-game-over-header-component", None) is not None
