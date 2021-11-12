import sys
from constants import SYMBOL
from db import create_engine, fetch_dataframe, plot_stats


def main():
    engine = create_engine(SYMBOL)
    dataframe = fetch_dataframe(SYMBOL, engine)
    if dataframe is None:
        raise Exception("Unable to fetch dataframe")
    if len(sys.argv) == 2 and (sys.argv[1] == "--graph" or sys.argv[1] == "-g"):
        plot_stats(SYMBOL, dataframe, "Price")
    else:
        print(dataframe)


if __name__ == "__main__":
    main()
