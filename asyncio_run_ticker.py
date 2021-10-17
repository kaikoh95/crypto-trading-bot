import asyncio
import sys
from db import create_engine
from constants import SYMBOL
from binance_helpers import init_binance_socket_manager, read_binance_symbol


async def main():
    symbol = SYMBOL
    if len(sys.argv) == 2:
        symbol = sys.argv[1]
    engine = create_engine(symbol)
    bm = await init_binance_socket_manager()
    await read_binance_symbol(bm, engine, symbol)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
