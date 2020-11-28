from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stockclass import Stock
from stockclass import StockTransaction
import urllib.request, json

time_series_key = 'Time Series (Daily)'
open_key = '1. open'
high_key = '2. high'
low_key = '3. low'
close_key = '4. close'
volume_key = '5. volume'

def get_stock_transaction(api_code, security_name, stock_id , daily_data,date_key):
    cur_stock_transaction = StockTransaction(api_code,security_name,stock_id,date_key,daily_data[open_key], \
        daily_data[low_key],daily_data[high_key],daily_data[close_key],daily_data[volume_key])
    return cur_stock_transaction


def get_time_series(response_data):
    daily_data = response_data[time_series_key]
    return daily_data

def update_api_code(session,cur_stock):
    cur_stock.api_code = cur_stock.security_id
    session.commit()
    print("updating api code to " + cur_stock.security_id )



engine = create_engine('mysql://stockuser:delhi@localhost:3306/stocks')
Session = sessionmaker(bind=engine)
session = Session()
session_new = Session()
url_part1 = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=BSE:"
url_part2 = "&outputsize=full&apikey=MC90XH32PC655W2S"

for stock in session.query(Stock).filter(Stock.security_id == 'HDFC').order_by(Stock.id):
    stock.print_content()
    url = url_part1 + stock.api_code + url_part2 
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    if not time_series_key in data.keys():
        url = url_part1 + stock.security_id + url_part2 
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        update_api_code(session,stock)
   

    daily_data = get_time_series(data)
    keys_list = list(daily_data.keys())
    for index in range(0,1):
        date_key = keys_list[index]
        print(daily_data[date_key])
        stock_transaction = get_stock_transaction(stock.api_code,stock.security_name,stock.id,daily_data[date_key],date_key)
        stock_transaction.print_content()
        session_new.add(stock_transaction)
        
    session_new.commit()
    






