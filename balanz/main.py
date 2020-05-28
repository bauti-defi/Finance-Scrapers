from time import localtime, sleep
import datetime
from stocks import tickers 

#5:00:10 closing
market_close = datetime.datetime.now().replace(hour=17, minute=0, second=10,microsecond = 0)

def writeRatiosFile():
    ratios=open('./ratios.txt','w')
    for ticker in tickers:
        ratios.write(f"{ticker['symbol']},{ticker['ratio']}\n")
    ratios.close()

