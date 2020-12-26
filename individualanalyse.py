from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stockclass import Stock
from stockclass import StockTransaction
from datetime import datetime
import time
from datetime import datetime
import pandas as pd
from sqlalchemy.sql import func
from fibanoccilevel import FibannociLevel
import matplotlib.pyplot as plt

engine = create_engine('mysql://stockuser:delhi@localhost:3306/stocks')
Session = sessionmaker(bind=engine)
session = Session()

from_day = input("Please enter begin date  in YYYY-mm-dd format (2020-07-15)")
end_day = input("Please enter end date  in YYYY-mm-dd format (2020-07-15)")


stock_id = input("Enter stock id")

start_trade_day = datetime.strptime(from_day,"%Y-%m-%d")
end_trade_day = datetime.strptime(end_day,"%Y-%m-%d")

days =[]
prices =[]
resistance = 0.00
support = 999999.99
retracement_levels = [ 0.236,0.382,0.50,0.618]
for stock_transaction in session.query(StockTransaction).filter(and_(StockTransaction.stock_id == stock_id, \
    StockTransaction.trans_date>=start_trade_day,StockTransaction.trans_date <=end_day ) ).order_by(StockTransaction.trans_date):
    print(stock_transaction.close_price)
    days.append(stock_transaction.trans_date)
    prices.append(stock_transaction.close_price)
    if ( resistance <  stock_transaction.close_price):
        resistance = stock_transaction.close_price
    if ( support > stock_transaction.close_price) :
        support = stock_transaction.close_price
    

fib_level =  FibannociLevel()
fib_level.resistance = resistance
fib_level.support = support
fib_level.level0 = support +   (support * retracement_levels[0])
fib_level.level1 = support +   (support * retracement_levels[1])
fib_level.level2 = support +   (support * retracement_levels[2])
fib_level.level3 = support +   (support * retracement_levels[3])
fib_level.print_content()



plt.plot(days,prices)
plt.title('Daily Graph')
plt.xlabel('Days')
plt.ylabel('Prices')
plt.show()