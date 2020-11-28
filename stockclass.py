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

   

    def print_content(self):
        print(self.security_name)
        print(self.industry)

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

    




