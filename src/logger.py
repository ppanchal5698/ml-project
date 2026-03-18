import logging
import sys
from datetime import datetime
from pathlib import Path

# Try to use colorama for Windows support, fallback to ANSI codes
try:
    from colorama import Fore, Style, init

    init(autoreset=True)
except ImportError:

    class Fore:
        BLUE = "\033[94m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        RESET = "\033[0m"

    class Style:
        BRIGHT = "\033[1m"
        RESET_ALL = "\033[0m"


# 1. Define Custom SUCCESS Level
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


def success(self, message, *args, **kwargs):
    """Log a success message."""
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)


logging.Logger.success = success


# 2. Console Formatter (Colored)
class ColoredConsoleFormatter(logging.Formatter):
    """Custom formatter that adds ANSI color codes to terminal output ONLY."""

    LEVEL_COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.BLUE,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED,
        SUCCESS_LEVEL: Fore.GREEN,
    }

    def format(self, record):
        # Format the standard message first
        msg = super().format(record)

        # Apply color wrapping to the entire string
        color = self.LEVEL_COLORS.get(record.levelno, "")
        if color:
            return f"{Style.BRIGHT}{color}{msg}{Style.RESET_ALL}"
        return msg


# 3. Logger Initialization
def get_logger(name: str = "app_logger", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(level)

    # Calculate current time constraints
    now = datetime.now()

    # Requirement 1 & 2: Create /logs/MM-YYYY/ folder
    month_year = now.strftime("%m-%Y")
    log_dir = Path(__file__).parent / "logs" / month_year
    log_dir.mkdir(parents=True, exist_ok=True)

    # Requirement 3: Create DD_app.log file
    day_file = now.strftime("%d_app.log")
    log_file_path = log_dir / day_file

    # Base formatter structure
    log_format = "[%(asctime)s] %(levelname)s - %(name)s:%(lineno)d - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Requirement 4: Differentiated Handlers
    # FILE HANDLER - Strictly Plain Text
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
    file_handler.setFormatter(file_formatter)

    # CONSOLE HANDLER - ANSI Colored
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = ColoredConsoleFormatter(fmt=log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)

    # Attach handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Default root logger export
logger = get_logger()

# if __name__ == "__main__":
#     logger.info("Info message - written plain to file, BLUE in terminal.")
#     logger.success("Success message - written plain to file, GREEN in terminal.")
#     logger.warning("Warning message - written plain to file, YELLOW in terminal.")
#     logger.error("Error message - written plain to file, RED in terminal.")
