#This is storage.py here we need to store incomming data into the databse of GATEWAY

from database import Session
from models import DeviceTable
import json

def Give_Obj(the_obj):
	store=DeviceTable(
	node_id=the_obj.node_id,
	node_uid=the_obj.node_uid,
	node_type=the_obj.node_type,
	node_firmware=the_obj.firmware_ver,
	node_location=the_obj.location,
	node_plugin=the_obj.plugin,
	data=json.dumps(the_obj.data)
	)
	return store

def store_in_db(obj):
	db=Session()
	db.add(obj)
	db.commit()
	db.close()

	return "Stored in database without fail!!"
