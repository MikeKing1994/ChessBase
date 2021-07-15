from datetime import datetime
import logging


def generate_log_file_name():
    current_date_time = str(datetime.now())
    formatted_date = current_date_time.replace(":", "_").replace(".", "_").replace(" ", "_")
    return f'C://ChessBotLogs/{formatted_date}.log'


def set_up_log_file():
    file_name = generate_log_file_name()
    logging.basicConfig(filename=file_name, level=logging.INFO)