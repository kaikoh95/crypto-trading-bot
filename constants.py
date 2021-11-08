from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
ENV = os.environ.get("ENV") or "development"
IS_PROD = True if ENV == "production" else False
KU_KEY = os.environ.get("KU_KEY")
KU_SECRET = os.environ.get("KU_SECRET")
KU_PASS = os.environ.get("KU_PASS")
KU_URL = os.environ.get("KU_URL")

DB_FOLDER = "db_streams"

# Symbols
BTCUSDT = "BTCUSDT"
SHIBBUSD = "SHIBBUSD"
NANOBUSD = "NANOBUSD"
SOLBNB = "SOLBNB"
BTCSTUSD = "BTCSTUSD"
BTCBUSD = "BTCBUSD"
ADABUSD = "ADABUSD"
DARBUSD = "DARBUSD"

# Main symbol to use
SYMBOL = DARBUSD
