from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from shared import Position


def get_chess_dot_com_square_name_from_position(pos):
    x = str(pos.X + 1)
    y = str(pos.Y + 1)
    return f'square-{x}{y}'


def move_piece_internal(driver, action_chains, move_from_class, move_to_class):
    move_from = driver.find_element_by_class_name(move_from_class)
    move_from.click()

    move_to = driver.find_element_by_class_name(move_to_class)
    action_chains.drag_and_drop(move_from, move_to).perform()


def move_piece(driver, action_chains, from_position, to_position):
    from_class = get_chess_dot_com_square_name_from_position(from_position)
    to_class = get_chess_dot_com_square_name_from_position(to_position)
    move_piece_internal(driver, action_chains, from_class, to_class)


def wait_until_board_loaded(driver, wait):
    wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "square-42"))
    )


def go_to_chess_dot_com():
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

    wait_until_board_loaded(driver, wait)

    action_chains = ActionChains(driver)
    move_piece(driver, action_chains, Position(3, 1), Position(3, 3))

    print(choose_button)
    #driver.close()