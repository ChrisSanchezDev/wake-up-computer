import logging
import os
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

# ----- Adjust this section per project -----
RELATIVE_LOG_FILE = 'scripts/wake-up-computer/logs/wake-up-computer.log'
LOGGER_NAME = 'wake-up-computer'
# -------------------------------------------

home_dir = os.path.expanduser('~')
LOG_FILE = os.path.join(home_dir, RELATIVE_LOG_FILE)

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

LOG_STATE = os.getenv('LOG_STATE', 'info').lower()

MAX_BYTES = 5 * 1024 * 1024 # 5MB
BACKUP_COUNT = 3

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

rotate_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=MAX_BYTES,
    backupCount=BACKUP_COUNT
)
rotate_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger(LOGGER_NAME)
logger.addHandler(rotate_handler)

console_logger = logging.getLogger(f'{LOGGER_NAME}.console')
console_logger.addHandler(rotate_handler)
console_logger.addHandler(console_handler)

if LOG_STATE == 'debug':
    logger.setLevel(logging.DEBUG)
    console_logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
    console_logger.setLevel(logging.INFO)