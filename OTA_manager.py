import requests
import os

from GateWayDetails import server_url, GateWay_ID, GateWay_Location
from database import Session
from models import OTAUpdate

db = Session()

OTA_DIR = "OTA_files"
os.makedirs(OTA_DIR, exist_ok=True)

url_addon = f"/firmware/{GateWay_Location}/{GateWay_ID}"


def check_ota():
    url = server_url.rstrip("/") + url_addon

    try:
        print("Checking OTA from:", url)

        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            print("OTA check failed:", res.status_code)
            print(res.text)
            return

        data = res.json()

        if data.get("count", 0) == 0:
            print("No OTA updates")
            return

        for item in data["data"]:
            node_id = item["target_node"]
            file_name = item["file_name"]
            download_url = item["download_url"]

            # 🔥 FIXED URL JOIN
            full_url = server_url.rstrip("/") + "/" + download_url.lstrip("/")

            local_path = os.path.join(OTA_DIR, file_name)

            print("\n--- OTA TASK ---")
            print("Node:", node_id)
            print("File:", file_name)
            print("Download URL:", full_url)

            # 🔒 check duplicate
            exists = db.query(OTAUpdate).filter(
                OTAUpdate.node_id == node_id,
                OTAUpdate.update_url == full_url
            ).first()

            if exists:
                print("Already exists in DB, skipping")
                continue

            # 🔥 DOWNLOAD FILE
            if os.path.exists(local_path):
                print("File already exists locally")
            else:
                try:
                    print("Downloading...")

                    r = requests.get(full_url, stream=True, timeout=10)

                    print("Download status:", r.status_code)

                    if r.status_code != 200:
                        print("Download failed:", r.text)
                        continue

                    with open(local_path, "wb") as f:
                        for chunk in r.iter_content(1024):
                            if chunk:
                                f.write(chunk)

                    print("Downloaded successfully")

                except Exception as e:
                    print("Download error:", e)
                    continue

            # 💾 STORE IN DB
            new_entry = OTAUpdate(
                node_id=node_id,
                update_url=full_url,
                firmware_path=local_path,
                status="pending"
            )

            db.add(new_entry)
            db.commit()

            print(f"OTA added → {node_id} : {file_name}")

    except Exception as e:
        print("OTA check error:", e)
