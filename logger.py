from libs.time import formatted_date
import sys
import os
from enum import IntEnum

class Ansi(IntEnum):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47


# Received permission directly from him to use it. Just figured it looks cool.
# Made some optimisations to it.
__name__ = "LoggerModule"
__author__ = "lenforiee"

DEBUG = "debug" in sys.argv

# Windows support
# activated only when os name is nt (windows)
if os.name == "nt":
    from ctypes import windll

    windll.kernel32.SetConsoleMode(windll.kernel32.GetStdHandle(-11), 7)


def log_message(content: str, l_type: str, bg_col: str):
    """Creates the final string and writes it to console.

    Args:
        content (str): The main text to be logged to console.
        l_type (str): The type of the log that will be displayed to the user.
        bl_col (str): The background colour for the `l_type`.
    """

    # Print to console. Use this as faster ig.
    sys.stdout.write(
        f"\033[37m{bg_col}[{l_type}]\033[49m - "
        f"[{formatted_date()}] {content}\033[39m\n"
    )


def custom_log(message: str, header: str, colour: Ansi):
    """Prints custom log with custom header and colour"""
    return log_message(message, header, f"\033[{colour.value}m")


def debug(message: str):
    if DEBUG:
        return log_message(message, "DEBUG", "\033[43m")


def info(message: str):
    return log_message(message, "INFO", "\033[42m")


def error(message: str):
    # Log errors to file.
    write_log_file(message)
    return log_message(message, "ERROR", "\033[41m")


def warning(message: str):
    return log_message(message, "WARNING", "\033[44m")


def check_log_file() -> bool:
    """Checks if a valit log file exists that can be written to."""

    return os.path.exists("err.log")


def ensure_log_file():
    """Ensures that a log file is present that can be written to."""

    os.mknod("err.log")


def write_log_file(msg: str, timestamp: bool = True):
    """Appends a message to the log file."""

    with open("err.log", "a+") as f:
        if timestamp:
            f.write(f"[{formatted_date()}] {msg}\n")
        else:
            f.write(msg)
