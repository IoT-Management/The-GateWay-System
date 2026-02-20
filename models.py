#Make Table
#this is model.py

from sqlalchemy import Column,Integer,String,DateTime,Text
from database import Base,eng
from datetime import datetime

#creating Table
class DeviceTable(Base):
	__tablename__="Nodes"
	ID=Column(Integer,primary_key=True,index=True)
	node_id=Column(String,index=True)
	EntryTime=Column(DateTime,default=datetime.utcnow)
	data=Column(Text)

Base.metadata.create_all(bind=eng)
