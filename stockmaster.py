import csv
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from stockclass import Stock

with open('Equity.csv', 'r') as file:
    reader = csv.reader(file, delimiter = ',')
    title_read = False
    k =1 
    engine = create_engine('mysql://stockuser:delhi@localhost:3306/stocks')
    Session = sessionmaker(bind=engine)
    session = Session()

    for row in reader:
        if (title_read is True):
            cur_stock = Stock(row)
            #cur_stock.save_from_list(row)
            cur_stock.print_content()
            session.add(cur_stock)
        else:
             print(row) 
        title_read = True


    session.commit()