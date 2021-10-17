from binance import AsyncClient, BinanceSocketManager
from constants import API_KEY, API_SECRET
from db import create_frame


async def binance_client():
    return await AsyncClient.create(api_key=API_KEY, api_secret=API_SECRET)


async def init_binance_socket_manager():
    client = await binance_client()
    return BinanceSocketManager(client)


async def read_binance_symbol(bm, engine, symbol):
    ts = bm.trade_socket(symbol)
    async with ts as tscm:
        while True:
            msg = await tscm.recv()
            frame = create_frame(msg)
            frame.to_sql(symbol, engine, if_exists="append", index=False)
            print(frame)
