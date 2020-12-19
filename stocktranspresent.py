from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stockclass import Stock
from stockclass import StockTransaction
import urllib.request, json
from datetime import datetime
import time

time_series_key = 'Time Series (Daily)'
open_key = '1. open'
high_key = '2. high'
low_key = '3. low'
close_key = '4. close'
volume_key = '5. volume'

def get_stock_transaction(api_code, security_name, stock_id , daily_data,date_key):
    trade_day = datetime.strptime(date_key,"%Y-%m-%d")
    cur_stock_transaction = StockTransaction(api_code,security_name,stock_id,trade_day,float(daily_data[open_key]), \
        float(daily_data[low_key]),float(daily_data[high_key]),float(daily_data[close_key]),daily_data[volume_key])
    return cur_stock_transaction


def get_time_series(response_data):
    if time_series_key in response_data:
        daily_data = response_data[time_series_key]
        return daily_data
    else:
        return ''

def update_tracked(session,cur_stock):
    cur_stock.is_tracked = True
    session.commit()
    print("updating is trakced to true " + cur_stock.security_id )


engine = create_engine('mysql://stockuser:delhi@localhost:3306/stocks')
Session = sessionmaker(bind=engine)
session = Session()
url_part1 = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BSE:"
url_part2 = "&outputsize=120&apikey=3N39E9EDEQGEWWBM"    

#MC90XH32PC655W2S 3N39E9EDEQGEWWBM
# select * from  stock_master where groupc ='A ' or groupc = 'B ' and id < 700 -- upto Nov 27 

for stock in session.query(Stock).filter(and_(Stock.groupc == 'X ' ,Stock.id < 2000,Stock.id >= 1812 )).order_by(Stock.id):
    #stock.print_content()
    url = url_part1 + stock.api_code + url_part2
    print(stock.security_name) 
    print(stock.id) 
    
    time.sleep(2)
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    daily_data = get_time_series(data)
    if (daily_data == ''):
        continue
    keys_list = ["2020-12-07","2020-12-08","2020-12-09","2020-12-10","2020-12-11","2020-12-14","2020-12-15","2020-12-16","2020-12-17","2020-12-18"]
    for index in range(0,len(keys_list)):
        date_key = keys_list[index]
        print(date_key)
        if(date_key in daily_data):
            print(daily_data[date_key])
            stock_transaction = get_stock_transaction(stock.api_code,stock.security_name,stock.id,daily_data[date_key],date_key)
            session.add(stock_transaction)
            session.commit()
            update_tracked(session,stock)
        #stock_transaction.print_content()
        
    
