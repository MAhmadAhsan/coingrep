from pathlib import Path

APP_NAME = "CoinGrep"
APP_SYMBOL = "coingrep"
APP_VERSION = "1.0.0"

HOME_DIR = Path.home()

LOGS_DIR = HOME_DIR / f".{APP_SYMBOL}" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_PATH = LOGS_DIR / f"{APP_VERSION}.log"


DB_DIR = HOME_DIR / f".{APP_SYMBOL}" / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / f"{APP_SYMBOL}.db"