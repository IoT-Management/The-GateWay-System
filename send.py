#Send Data to main server
import requests
from read import read_all_data,delete_from_db
import json
from GateWayDetails import GateWay_ID,GateWay_Location,server_url,post_auth

url="https://api.yashkriti.online/gateway_send"

def send_to_server():
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
			response=requests.post(url,json=payload,timeout=5)
		
			if response.status_code==200:
				delete_from_db(i.ID)
			
			else:
				return "Server rejected data"
				

		except Exception as e:
			return f"{e}"
	return "Data Sent!"
