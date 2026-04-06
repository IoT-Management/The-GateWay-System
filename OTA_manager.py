import requests
import os

from GateWayDetails import server_url, GateWay_ID, GateWay_Location
from database import session
from models import OTAUpdate

db = session()

OTA_DIR = "OTA_files"
os.makedirs(OTA_DIR, exist_ok=True)

url_addon = f"/firmware/{GateWay_Location}/{GateWay_ID}"


def check_ota():
    url = server_url + url_addon

    try:
        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            print("OTA check failed:", res.status_code)
            return

        data = res.json()

        
        if data.get("count", 0) == 0:
            print("No OTA updates")
            return

        for item in data["data"]:
            node_id = item["target_node"]
            file_name = item["file_name"]
            download_url = item["download_url"]

            
            full_url = server_url + download_url

            
            local_path = os.path.join(OTA_DIR, file_name)

            
            exists = db.query(OTAUpdate).filter(
                OTAUpdate.node_id == node_id,
                OTAUpdate.update_url == full_url
            ).first()

            if exists:
                print(f"Already exists: {file_name}")
                continue

            
            new_entry = OTAUpdate(
                node_id=node_id,
                update_url=full_url,
                status="pending"
            )

            db.add(new_entry)
            db.commit()

            print(f"OTA added: {node_id} → {file_name}")

    except Exception as e:
        print("OTA check error:", e)
