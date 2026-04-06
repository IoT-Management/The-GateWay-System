from fastapi import FastAPI, Request
from fastapi.responses import FileResponse

from template import DeviceBlueprint
from storage import Give_Obj, store_in_db
from database import Base, session
from sqlalchemy import Column, Integer, String
from send import send_to_server
from GateWayDetails import server_url, post_auth
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from plugin_manager import find_plugin
from send_check import send_heartbeat

from models import OTAUpdate

import os


sch = BackgroundScheduler()
time_interval = 15


@asynccontextmanager
async def Start_stop(app: FastAPI):
    sch.start()
    yield
    sch.shutdown()


app = FastAPI(lifespan=Start_stop)

db = session()


OTA_DIR = "OTA_files"
os.makedirs(OTA_DIR, exist_ok=True)

@app.post("/data")
def rec(packet: DeviceBlueprint):
    print(packet.node_id)
    print(packet.data)

    TheObj = Give_Obj(packet)
    msg = None

    plg = find_plugin(packet)
    print(f"\n\n{plg}\n\n")

    if TheObj:
        msg = store_in_db(TheObj)

    return {"status": 200, "message": msg}


def sendTOserver():
    sent_status = send_to_server()
    heart = send_heartbeat()
    return {"status": 200, "sent_status": sent_status, "heartbeat": heart}


sch.add_job(sendTOserver, "interval", seconds=time_interval, max_instances=1)


@app.get("/ota/{node_id}")
def send_firmware(node_id: str):

    entry = db.query(OTAUpdate).filter(
        OTAUpdate.node_id == node_id,
        OTAUpdate.status == "pending"
    ).first()

    if not entry:
        return {"status": "no_update"}

    file_name = entry.update_url.split("/")[-1]
    file_path = os.path.join(OTA_DIR, file_name)

    if not os.path.exists(file_path):
        return {"error": "file not found on gateway"}


    entry.status = "in_progress"
    db.commit()

    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=file_name
    )


@app.post("/ota/complete/{node_id}")
def ota_complete(node_id: str):

    entry = db.query(OTAUpdate).filter(
        OTAUpdate.node_id == node_id,
        OTAUpdate.status == "in_progress"
    ).first()

    if not entry:
        return {"status": "no active OTA"}

    entry.status = "done"
    db.commit()

    return {"status": "OTA marked complete"}
