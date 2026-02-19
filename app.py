from fastapi import FastAPI
from template import DeviceBlueprint

app=FastAPI()

@app.post("/data")
def rec(packet:DeviceBlueprint ):
	print(packet.node_id)
	print(packet.data)
	
	return {"status": 200}
