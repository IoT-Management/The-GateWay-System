from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker, declaritive_base

#DataBase file creation
database_url="sqlite:///iot.db"

eng=create_engine(database_url,connect_args={"check_same_thread": False})

Session=sessionmaker(bind=eng)

Base=declaritive_base()




'''
This create as database in the relative path
Database_url is the url of database
eng=create_engine(url,connect_args={"check_same_thread":False}) // This makes an object telling that using these configration a database needs to worked or runned with check_same_thread:False tells that dont see how many devices are asking or reffering to same device let all acess it

sessionmaker() makes one more object which lets to work or edit in database
declaritive_base tells the class that this class is a database work
'''
