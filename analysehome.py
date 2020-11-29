from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stockclass import Stock
from stockclass import StockTransaction
import urllib.request, json
from datetime import datetime
import pandas as pd

engine = create_engine('mysql://stockuser:delhi@localhost:3306/stocks')
Session = sessionmaker(bind=engine)
session = Session()

from_day = input("Please enter begin date  in YY-mm-dd format")
end_day = input("Please enter end date  in YY-mm-dd format")

start_trade_day = datetime.strptime(from_day,"%Y-%m-%d")
end_trade_day = datetime.strptime(end_day,"%Y-%m-%d")
all_records =[] 
for stock in session.query(Stock).filter( Stock.groupc == 'A ').order_by(Stock.id):
    start_price = 1
    end_price = 1
    for trans in  session.query(StockTransaction).filter(and_(StockTransaction.stock_id == stock.id, \
        StockTransaction.trans_date == start_trade_day )).order_by(StockTransaction.trans_date):
        start_price = trans.close_price
    
    for transClose in  session.query(StockTransaction).filter(and_(StockTransaction.stock_id == stock.id, \
        StockTransaction.trans_date == end_trade_day )).order_by(StockTransaction.trans_date):
        end_price = transClose.close_price

    percent_increase = ((end_price - start_price) / start_price) * 100
    #print("Stock = " +  stock.security_name  + ":start=" + str(start_price) + ": end=" + str(end_price) + ":incr=" + str(percent_increase))
    ind_record =[stock.security_name,stock.industry,start_price,end_price,percent_increase]
    all_records.append(ind_record)

df = pd.DataFrame(all_records,columns=['Stock','Industry','Start','End','Percent'])
print(type(df.sort_values(by=['Percent'])))
#print(df) 

