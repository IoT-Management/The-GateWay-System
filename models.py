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
	node_uid=Column(String,index=True)
	node_type=Column(String,index=True)
	node_firmware=Column(String,index=True)
	node_location=Column(String,index=True)
	node_plugin=Column(String,index=True)
	EntryTime=Column(DateTime,default=datetime.utcnow)
	data=Column(Text)



class OTAUpdate(Base):
    __tablename__ = "ota_updates"

    id = Column(Integer, primary_key=True, index=True)

    node_id = Column(String, index=True)

    update_url = Column(String)    
    firmware_path = Column(String) 

    status = Column(String, default="pending") 


Base.metadata.create_all(bind=eng)
