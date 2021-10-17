# crypto-trading-bot
Automated crypto trading bot as adapted from [Algovibes](https://www.youtube.com/watch?v=rc_Y6rdBqXM&amp;t=451s&amp;ab_channel=Algovibes).

### Pre-requisites
Ensure that you have created a [Binance API key](https://www.binance.com/en/my/settings/api-management) before proceeding.

Ensure that you are running on Python 3.6 and above.

### Setup
Recommended to use virtual environment to run the files not required.
```
# copy and populate your Binance API credentials in the env file
cp test.env .env
# ENV in .env takes either "development" or "production"

# install dependencies
pip install -r requirements.txt
```

### Getting a ticker's data
Fetches the data from Binance and stores in sqlite.
```
# you can pass in an argument 
# consisting of the ticker that you want
$ python asyncio_run_ticker.py BTCUSDT

# or just run the command
# with the preset symbol defined in constant.py
$ python asyncio_run_ticker.py
```

### Processing/Reading ticker's data
```
# show all entries of the ticker in the sqlite stream
$ python read_db.py

# show entries as a graph
$ python read_db.py --graph
```

### Executing the trade bot
WARNING: Please check that you have set the correct ENV in .env file before running the following.
```
$ python trade_bot.py
```