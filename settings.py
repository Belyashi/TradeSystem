import datetime

DATABASE = 'mysql://root@localhost:3306/trade'

HISTORY_DAYS_BEFORE = 30
HISTORY_LOAD_BATCH = 2
HISTORY_UPDATE_TIMEDELTA = datetime.timedelta(minutes=1)

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 3000

STOCKS = './stocks.json'
