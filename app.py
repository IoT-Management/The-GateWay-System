from fastapi import FastAPI,Request
from template import DeviceBlueprint
from storage import Give_Obj,store_in_db
from database import Base
from sqlalchemy import Column,Integer,String
from send import send_to_server
from  GateWayDetails import server_url, post_auth
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from plugin_manager import find_plugin
sch=BackgroundScheduler()
time_interval=15
@asynccontextmanager
async def Start_stop(app:FastAPI):
	sch.start()
	yield
	sch.shutdown()

app=FastAPI(lifespan=Start_stop)

@app.post("/data")
def rec(packet:DeviceBlueprint ):
	print(packet.node_id)
	print(packet.data)
	TheObj=Give_Obj(packet)
	msg=None
	plg=find_plugin(packet)
	print(f"\n\n{plg}\n\n")
	if TheObj:
		msg=store_in_db(TheObj)
	return {"status": 200,"message":msg}



def sendTOserver():
	sent_status=send_to_server()
	return {"status":200,"sent_status":sent_status}

sch.add_job(sendTOserver,"interval",seconds=time_interval,max_instances=1)
