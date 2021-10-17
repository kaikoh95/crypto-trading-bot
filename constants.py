from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
ENV = os.environ.get("ENV") or "development"
IS_PROD = True if ENV == "production" else False

DB_FOLDER = "db_streams"

# Symbols
BTCUSDT = "BTCUSDT"
SHIBBUSD = "SHIBBUSD"
SOLBNB = "SOLBNB"

# Main symbol to use
SYMBOL = SOLBNB
