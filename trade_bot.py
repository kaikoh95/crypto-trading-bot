from datetime import datetime
import pandas as pd
import asyncio
from binance_helpers import binance_client
from constants import SYMBOL, IS_PROD
from db import create_engine, fetch_dataframe


def formula(period):
    return (period.Price.pct_change() + 1).cumprod() - 1


def last_entry(cumulative_return):
    return cumulative_return[cumulative_return.last_valid_index()]


def algo(change, threshold, loss_threshold, loss_count, profit_count):
    should_close_order = True
    if change >= threshold:
        print(f"Open position has risen by {threshold * 100}%, placing SELL order at MARKET price to close position.")
        profit_count += 1
    elif change < -loss_threshold:
        print(f"Open position has dropped by {loss_threshold * 100}%, placing SELL order at MARKET price to close position.")
        loss_count += 1
    else:
        should_close_order = False
    return should_close_order, loss_count, profit_count


async def trend_following_strategy(symbol, threshold, loss_threshold, entry, period_in_seconds, quantity, loss_count=0, profit_count=0):
    """Trend-following: If crypto rising by entry% = Buy. Exit when profit or loss more than threshold%.
    """
    order = None
    open_position = False

    if IS_PROD:
        print("WARNING: Running this will place REAL orders.")
    else:
        print("Running this will only place TEST orders.")

    engine = create_engine(symbol)
    client = await binance_client()

    print(f"Awaiting {symbol} to rise by {entry * 100}%")
    while not open_position:
        df = fetch_dataframe(symbol, engine)
        if df is None:
            break
        period = df.iloc[-period_in_seconds:]
        cumulative_return = formula(period)
        if last_entry(cumulative_return) > entry:
            print(f"{symbol} has risen by {entry * 100}% or more, placing BUY order at MARKET price to open position.")
            if IS_PROD:
                order = await client.create_order(symbol=symbol, side="BUY", type="MARKET", quantity=quantity)
            else:
                order = await client.create_test_order(symbol=symbol, side="BUY", type="MARKET", quantity=quantity)
            print(order)
            open_position = True

    print(f"Awaiting position for {symbol} to rise by {threshold * 100}% or drop by {loss_threshold * 100}%.")
    while open_position and order is not None:
        df = fetch_dataframe(symbol, engine)
        if df is None:
            break
        since_buy = df.loc[df.Time > pd.to_datetime(order["transactTime"], unit="ms")]
        if len(since_buy) > 1:
            return_since_buy = formula(since_buy)
            should_close_order, loss_count, profit_count = algo(last_entry(return_since_buy), threshold,
                                                                loss_threshold, loss_count, profit_count)
            if should_close_order:
                if IS_PROD:
                    order = await client.create_order(symbol=symbol, side="SELL", type="MARKET", quantity=quantity)
                else:
                    order = await client.create_test_order(symbol=symbol, side="SELL", type="MARKET", quantity=quantity)
                print(order)
                open_position = False

    # close client to prevent errors from unclosed sockets
    await client.close_connection()

    return loss_count, profit_count


async def main():
    repeat_strategy = True
    loss_count = 0
    profit_count = 0
    trade_count = 0
    start = datetime.now()
    cutoff = datetime.now()

    while repeat_strategy:
        loss_count, profit_count = await trend_following_strategy(
            symbol=SYMBOL, threshold=0.005, loss_threshold=0.025, entry=0.001, period_in_seconds=60, quantity=0.001,
            loss_count=loss_count, profit_count=profit_count)
        trade_count += 1
        print(f"{profit_count} x profit | {loss_count} x loss")
        if loss_count > 1 or profit_count > 10:
            repeat_strategy = False
            cutoff = datetime.now()
    print(f"""Overall
Start time: {start}
Cutoff time: {cutoff}
Total trades: {trade_count}
Profitable trades: {profit_count}
Loss trades: {loss_count}""")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
