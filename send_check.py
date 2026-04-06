from datetime import datetime
from GateWayDetails import GateWay_ID,GateWay_Location,server_url,post_auth
import requests
def send_heartbeat():
    payload = {
        "gateway_id": GateWay_ID,
        "gateway_location": GateWay_Location,
        "esp_data": {
            "node_id": "__heartbeat__",   
            "gateway_time": datetime.utcnow().isoformat(),
            "esp_data": {}
        }
    }

    try:
        response = requests.post(
            f"{server_url}/{post_auth}",
            json=payload,
            timeout=5
        )
        return response.status_code

    except Exception as e:
        return str(e)
