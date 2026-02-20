#This is storage.py here we need to store incomming data into the databse of GATEWAY

from database import Session
from models import DeviceTable
import json

def Give_Obj(id,dat):
	store=DeviceTable(
	node_id=id,
	data=json.dumps(dat)
	)
	return store

def store_in_db(obj):
	db=Session()
	db.add(obj)
	db.commit()
	db.close()

	return "Stored in database without fail!!"
