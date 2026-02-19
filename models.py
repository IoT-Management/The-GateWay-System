#Make Table
#this is model.py

from sqlalchemy import Column,Integer,String,DateTime,Text
from database import Base
from datetime import datetime

#creating Table
class DeviceTable(Base):
	__tablename__="Nodes"
	ID=Column(Integer,primary_key=True,index=True)
	nodeID=Column(String,index=True)
	EntryTime=Column(DateTime,default=datetime.utcnow)
	Data=Column(Text)

