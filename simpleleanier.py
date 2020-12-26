import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stockclass import Stock
from stockclass import StockTransaction
from datetime import datetime
import time
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split

engine = create_engine('mysql://stockuser:delhi@localhost:3306/stocks')
Session = sessionmaker(bind=engine)
session = Session()

from_day = input("Please enter begin date  in YYYY-mm-dd format (2020-07-15)")
end_day = input("Please enter end date  in YYYY-mm-dd format (2020-07-15)")
stock_id = input("Enter stock id")

start_trade_day = datetime.strptime(from_day,"%Y-%m-%d")
end_trade_day = datetime.strptime(end_day,"%Y-%m-%d")


#x = np.array([5, 15, 25, 35, 45, 55]).reshape((-1, 1))
#y = np.array([5, 20, 14, 32, 22, 38])


days =[]
prices =[]
day_count = 0
for stock_transaction in session.query(StockTransaction).filter(and_(StockTransaction.stock_id == stock_id, \
    StockTransaction.trans_date>=start_trade_day,StockTransaction.trans_date <=end_day ) ).order_by(StockTransaction.trans_date):
    print(stock_transaction.close_price)
    day_count = day_count +1
    days.append(day_count )
    prices.append(stock_transaction.close_price)


data_df = pd.DataFrame({"day":days,"price":prices}) 

y = np.asarray(data_df['price'])
X = data_df[['day']]
X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=.7,random_state=42)

model = LinearRegression() #create linear regression object
model.fit(X_train, y_train) #train model on train data
model.score(X_train, y_train) #check score
print ('Coefficient: \n', model.coef_)
print ('Intercept: \n', model.intercept_)
x_predict = np.array([day_count + 1]).reshape((-1, 1))
y_predict = model.predict(x_predict)
print ('predict ; \n' , y_predict)