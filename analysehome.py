from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stockclass import Stock
from stockclass import StockTransaction
import urllib.request, json
from datetime import datetime
import pandas as pd
from sqlalchemy.sql import func

engine = create_engine('mysql://stockuser:delhi@localhost:3306/stocks')
Session = sessionmaker(bind=engine)
session = Session()

from_day = input("Please enter begin date  in YYYY-mm-dd format (2020-07-15)")
end_day = input("Please enter end date  in YYYY-mm-dd format (2020-07-15)")

start_trade_day = datetime.strptime(from_day,"%Y-%m-%d")
end_trade_day = datetime.strptime(end_day,"%Y-%m-%d")
all_records =[] 
for stock in session.query(Stock).filter(Stock.is_tracked == True ).order_by(Stock.id):
    start_price = 1
    end_price = 1
    for trans in  session.query(StockTransaction).filter(and_(StockTransaction.stock_id == stock.id, \
        StockTransaction.trans_date == start_trade_day )).order_by(StockTransaction.trans_date):
        start_price = trans.close_price
    
    for transClose in  session.query(StockTransaction).filter(and_(StockTransaction.stock_id == stock.id, \
        StockTransaction.trans_date == end_trade_day )).order_by(StockTransaction.trans_date):
        end_price = transClose.close_price

    aggrValue =  session.query(func.max(StockTransaction.close_price),func.min(StockTransaction.close_price),func.avg(StockTransaction.close_price)).filter(and_(StockTransaction.stock_id == stock.id, \
        StockTransaction.trans_date <= end_trade_day, StockTransaction.trans_date >= start_trade_day)).all()

     
    min_price = aggrValue[0][1]
    max_price = aggrValue[0][0]
    avg_price = aggrValue[0][2]
    
    percent_variation =1
    percent_increase = ((end_price - start_price) / start_price) * 100
    if ( not (min_price  is None) and  not (max_price  is None)):
        percent_variation = ((max_price - min_price) / min_price) * 100
    #print("Stock = " +  stock.security_name  + ":start=" + str(start_price) + ": end=" + str(end_price) + ":incr=" + str(percent_increase))
    ind_record =[stock.id,stock.security_name,stock.industry,start_price,end_price,percent_increase,min_price,max_price,avg_price,percent_variation]
    if (start_price != 1 and end_price != 1):
        all_records.append(ind_record)

df = pd.DataFrame(all_records,columns=['Id','Stock','Industry','Start','End','Percent','Min','Max','Avg','Var'])
sorted_rows = df.sort_values(by=['Percent'],ascending=False)
sorted_rows.to_csv('f3.csv',index=False)
#for currow in sorted_rows.iterrows():
    #print (currow)
    #print(currow['Stock'] + ' ' + currow['Industry'] + ' ' + currow['Start'] + ' ' + currow['End'] + ' ' +  currow['Percent']  )
#print(df)

