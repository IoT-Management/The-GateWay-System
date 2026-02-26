from database import Session
from models import  DeviceTable

node_dict={}
def read_all_data():
	db=Session()
	entries=db.query(DeviceTable).all()
	db.close()
	for i in entries:
		
		print(i.node_id)
		print(i.data)
	return entries

def delete_from_db(entry_id:int):
	db=Session()
	
	try:
		obj= db.query(DeviceTable).filter(DeviceTable.ID==entry_id).delete()
		
		db.commit()
	finally:
		db.close()
