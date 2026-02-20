from fastapi import FastAPI,Request
from template import DeviceBlueprint
from storage import Give_Obj,store_in_db

app=FastAPI()
app.post("/data")
def rec(packet:DeviceBlueprint ):
	print(packet.node_id)
	print(packet.data)
	TheObj=Give_Obj(packet.node_id,packet.data)
	if TheObj:
		msg=store_in_db(TheObj)
	return {"status": 200,"message":msg}
