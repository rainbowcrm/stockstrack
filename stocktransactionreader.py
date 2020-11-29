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
    daily_data = response_data[time_series_key]
    return daily_data

def update_api_code(session,cur_stock):
    cur_stock.api_code = cur_stock.security_id
    session.commit()
    print("updating api code to " + cur_stock.security_id )

def update_group_code(session,cur_stock):
    cur_stock.groupc = 'UNID'
    session.commit()
    print("updating Group C to UNID for " + cur_stock.security_id )


engine = create_engine('mysql://stockuser:delhi@localhost:3306/stocks')
Session = sessionmaker(bind=engine)
session = Session()
url_part1 = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BSE:"
url_part2 = "&outputsize=full&apikey=3N39E9EDEQGEWWBM"    

#MC90XH32PC655W2S 3N39E9EDEQGEWWBM

for stock in session.query(Stock).filter(and_(Stock.id >= 4000, Stock.id < 4400 , Stock.groupc == 'A ')).order_by(Stock.id):
    #stock.print_content()
    url = url_part1 + stock.api_code + url_part2
    print(stock.security_name) 
    time.sleep(2)
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    if not time_series_key in data.keys():
        url = url_part1 + stock.security_id + url_part2
        print('searching on security id')
        time.sleep(2) 
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        if  time_series_key in data.keys():
            update_api_code(session,stock)
        else:
            update_group_code(session,stock)
            continue

    daily_data = get_time_series(data)
    keys_list = list(daily_data.keys())
    for index in range(0,100):
        date_key = keys_list[index]
        print(date_key)
        print(daily_data[date_key])
        stock_transaction = get_stock_transaction(stock.api_code,stock.security_name,stock.id,daily_data[date_key],date_key)
        session.add(stock_transaction)
        session.commit()
        #stock_transaction.print_content()
        
    
    






