from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stock_master"
    id = Column(Integer, primary_key=True)
    security_code=Column(String)
    issuer_name =Column(String)
    security_id=Column(String)
    security_name=Column(String)
    status = Column(String)
    groupc=Column(String)
    face_value=Column(Float)
    isin_no=Column(String)
    industry=Column(String)
    api_code=Column(String)

    def __init__(self,list_of_values):
        self.security_code=list_of_values[0]
        self.issuer_name =list_of_values[1]
        self.security_id=list_of_values[2]
        self.security_name=list_of_values[3]
        self.status = list_of_values[4]
        self.groupc=list_of_values[5]
        self.face_value=list_of_values[6]
        self.isin_no=list_of_values[7]
        self.industry=list_of_values[8]
        self.api_code=self.security_id

   

    def print_content(self):
        print(self.security_name)
        print(self.api_code)
        print(self.id)

    def save_from_list(self,list_of_values):
        self.security_code=list_of_values[0]
        self.issuer_name =list_of_values[1]
        self.security_id=list_of_values[2]
        self.security_name=list_of_values[3]
        self.status = list_of_values[4]
        self.groupc=list_of_values[5]
        self.face_value=list_of_values[6]
        self.isin_no=list_of_values[7]
        self.industry=list_of_values[8]
        self.api_code=self.security_id

    


class StockTransaction(Base):
    __tablename__ = "stock_transaction"
    id = Column(Integer, primary_key=True)
    api_code = Column(String),
    security_name = Column(String),
    stock_id = Column(Integer,ForeignKey("stock_master.id"))
    trans_date = Column(DateTime),
    open_price = Column(Float),
    low_price =Column(Float),
    high_price = Column(Float),
    close_price =Column(Float),
    volume = Column(Float)
    #stock = relationship("Stock")

    def __init__ (self,api_code,security_name,stock_id,trans_date,open_price,low_price,high_price,close_price,volume ):
        self.api_code=api_code
        self.security_name=security_name
        self.stock_id=stock_id
        self.trans_date=trans_date
        self.open_price=open_price
        self.low_price=low_price
        self.high_price=high_price
        self.close_price=close_price
        self.volume=volume

    def print_content(self):
        print(self.security_name)
        print(self.api_code)
        print(self.open_price)
        print(self.close_price)
        print(self.stock_id)


        

