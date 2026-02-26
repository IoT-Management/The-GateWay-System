from fastapi import FastAPI,Request
from template import DeviceBlueprint
from storage import Give_Obj,store_in_db
from database import Base
from sqlalchemy import Column,Integer,String
from send import send_to_server
from  GateWayDetails import server_url, post_auth

app=FastAPI()
@app.post("/data")
def rec(packet:DeviceBlueprint ):
	print(packet.node_id)
	print(packet.data)
	TheObj=Give_Obj(packet.node_id,packet.data)
	if TheObj:
		msg=store_in_db(TheObj)

	
	return {"status": 200,"message":msg}


@app.post(f"/send-to-server")
def sendTOserver():
	sent_status=send_to_server()
	return {"status":200,"sent_status":sent_status}
