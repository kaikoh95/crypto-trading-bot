from datetime import datetime
from time import sleep

from kucoin.client import Trade
from constants import KU_KEY, KU_PASS, KU_SECRET, KU_URL
import asyncio


def init_client():
    return Trade(key=KU_KEY, secret=KU_SECRET, passphrase=KU_PASS, is_sandbox=False, url=KU_URL)


async def main():
    client = init_client()
    ticker = "KCS-USDT"
    amount = "22"  # "571.14288989"
    price = "20"  # "0.035"
    increment = 1.0  # 0.1
    qty = f"{float(amount) / float(price):.3f}"
    attempt = 0

    time = datetime.strptime("2021-11-08 21:05:15", "%Y-%m-%d %H:%M:%S")
    while time > datetime.now():
        print("waiting for time")
    print("start buy attempt", datetime.now())

    buy_order_id = None
    while buy_order_id is None and attempt < 3:
        try:
            buy_order_id = client.create_limit_order(ticker, "buy", qty, price).get("orderId")
            print("buy order placed", datetime.now())
            print("buy order placed", price, qty, ticker)
            if attempt < 2:
                sleep(0.3)
                fill_list = client.get_fill_list(tradeType="TRADE", orderId=buy_order_id).get("items")
                if len(fill_list) < 1:
                    cancel_order = client.cancel_order(buy_order_id)
                    raise Exception("cancelled buy order", cancel_order)
        except Exception as e:
            buy_order_id = None
            print(str(e))
            price = f"{float(price) + increment:.3f}"
            qty = f"{float(amount) // float(price)}"
            print("buy price refinement", price, qty, ticker)
            attempt += 1
            print("retry buy", datetime.now())
    print("buy_order_id", buy_order_id)
    print(3, datetime.now())

    price = f"{float(price) * 8}"
    sell_order_id = None
    attempt = 0
    while sell_order_id is None and buy_order_id is not None and attempt < 3:
        try:
            sell_order_id = client.create_limit_order(ticker, "sell", qty, price).get("orderId")
            print("sell order placed", datetime.now())
            print("sell order placed", price, qty, ticker)
            if attempt < 2:
                sleep(0.3)
                fill_list = client.get_fill_list(tradeType="TRADE", orderId=sell_order_id).get("items")
                if len(fill_list) < 1:
                    cancel_order = client.cancel_order(sell_order_id)
                    raise Exception("cancelled sell order", cancel_order)
        except Exception as e:
            sell_order_id = None
            print(str(e))
            price = f"{float(price) - increment:.3f}"
            print("sell price refinement", price, qty, ticker)
            attempt += 1
            print("retry buy", datetime.now())
    print("sell_order_id", sell_order_id)
    print(4, datetime.now())


if __name__ == "__main__":
    print("executing", datetime.now())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
