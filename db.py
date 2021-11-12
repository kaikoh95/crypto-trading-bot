import pandas as pd
import sqlalchemy
from constants import DB_FOLDER, SYMBOL
import matplotlib.pyplot as plt


def create_engine(symbol):
    engine = sqlalchemy.create_engine(f"sqlite:///{DB_FOLDER}/{symbol}-stream.db")
    return engine


def fetch_dataframe(symbol, engine):
    try:
        return pd.read_sql(symbol, engine)
    except Exception as e:
        print(f'Exception: {e}')
    return None


def plot_stats(symbol, dataframe, y_axis="Price", x_axis="Time"):
    dataframe.plot(title=symbol, x=x_axis, y=y_axis)
    plt.show()


def create_frame(msg):
    pd.set_option("precision", 18)
    df = pd.DataFrame([msg])
    df = df.loc[:, ["s", "E", "p"]]
    df.columns = ["symbol", "Time", "Price"]
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit="ms")
    return df
