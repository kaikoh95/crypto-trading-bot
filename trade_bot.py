import pandas as pd
import asyncio
from binance_helpers import binance_client
from constants import SYMBOL, ENV
from db import create_engine, fetch_dataframe


def formula(period):
    return (period.Price.pct_change() + 1).cumprod() - 1


def last_entry(cumulative_return):
    return cumulative_return[cumulative_return.last_valid_index()]


async def trend_following_strategy(symbol, threshold, entry, period_in_seconds, quantity, repeat=False, open_position=False):
    # Trend-following
    # if crypto rising by entry% = Buy
    # exit when profit or loss more than threshold%
    loss_count = 0
    if ENV == "production":
        print("WARNING: Running this will place REAL orders.")
    else:
        print("Running this will only place TEST orders.")
    engine = create_engine(symbol)
    client = await binance_client()
    print(f"Awaiting {symbol} to rise by {entry * 100}%")
    while not open_position:
        df = fetch_dataframe(symbol, engine)
        period = df.iloc[-period_in_seconds:]
        cumulative_return = formula(period)
        if last_entry(cumulative_return) > entry:
            print(f"{symbol} has risen by {entry * 100}% or more, placing BUY order at MARKET price to open position.")
            if ENV == "production":
                order = await client.create_order(symbol=symbol, side="BUY", type="MARKET", quantity=quantity)
            else:
                order = await client.create_test_order(symbol=symbol, side="BUY", type="MARKET", quantity=quantity)
            print(order)
            open_position = True

    print(f"Awaiting position for {symbol} to rise/drop by {threshold * 100}%")
    while open_position:
        df = fetch_dataframe(symbol, engine)
        since_buy = df.loc[df.Time > pd.to_datetime(order["transactTime"], unit="ms")]
        if len(since_buy) > 1:
            return_since_buy = formula(since_buy)
            if not (-threshold < last_entry(return_since_buy) < threshold):
                movement = "risen"
                if last_entry(return_since_buy) <= -threshold:
                    movement = "dropped"
                    loss_count += 1
                print(f"Open position has {movement} by {threshold * 100}%, placing SELL order at MARKET price to close position.")
                if ENV == "production":
                    order = await client.create_order(symbol=symbol, side="SELL", type="MARKET", quantity=quantity)
                else:
                    order = await client.create_test_order(symbol=symbol, side="SELL", type="MARKET", quantity=quantity)
                print(order)
                open_position = False

    # repeat strategy
    if repeat and loss_count < 4:
        await trend_following_strategy(symbol, threshold, entry, period_in_seconds, quantity)


async def main():
    await trend_following_strategy(symbol=SYMBOL, threshold=0.005, entry=0.001, period_in_seconds=60, quantity=0.5, repeat=True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
