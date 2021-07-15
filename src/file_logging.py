from datetime import datetime


def generate_log_file_name():
    current_date_time = str(datetime.now())
    formatted_date = current_date_time.replace(":", "_").replace(".", "_").replace(" ", "_")
    return f'{formatted_date}.txt'
