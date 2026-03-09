#Send Data to main server
import requests
from read import read_all_data,delete_from_db
import json
from GateWayDetails import GateWay_ID,GateWay_Location,server_url,post_auth

url=server_url

def check_connection():
	try:
		res=requests.get(url+"/GateWay/Health",timeout=5)
		return res.status_code == 200
	except Exception:
		return False
	
def send_to_server():
	if check_connection():
		data=read_all_data()
		for i in data:
			payload={
				"gateway_id":GateWay_ID,
				"gateway_location":GateWay_Location,
				"esp_data":{
					"node_id":i.node_id,
					"gateway_time":str(i.EntryTime),
					"esp_data":json.loads(i.data)
						}
			}
	
			try:
				response=requests.post(url+f"/{post_auth}",json=payload,timeout=5)
		
				if response.status_code==200:
					delete_from_db(i.ID)
			
				else:
					return "Server rejected data"
				

			except Exception as e:
				return f"{e}"
		return "Data Sent!"

	else:
		return "Data not sent"
