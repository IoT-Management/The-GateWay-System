


# The-GateWay-System

> The local intelligence layer of The GateWay System IoT platform.
> Runs on a Raspberry Pi, BeagleBone Black, or any Linux device — receives data from ESP32 nodes, runs automation plugins, manages OTA updates, and syncs to the cloud.

## What is this?

The GateWay System is the "brain" of a local-first IoT architecture. Instead of ESP32 devices connecting directly to the cloud, they talk to this gateway running on your local network.

The gateway handles:
- Receiving sensor data from multiple ESP32 nodes over HTTP
- Running automation plugins (e.g. turn on LEDs if temperature > 50°C)
- Buffering data locally in SQLite when the cloud is unreachable
- Syncing buffered data to a cloud server every 15 seconds
- Polling the cloud server for OTA firmware updates every 30 seconds
- Serving firmware files to ESP32 nodes for OTA installation
- Sending periodic heartbeats to the cloud server

## Architecture
```

ESP32 Nodes  →  Gateway (This Repo)  →  Cloud Server
↓
SQLite Local DB
↓
Automation Plugins

```
## Tech Stack

- **Python 3**
- **FastAPI** — REST API server
- **SQLAlchemy** — ORM with SQLite local database
- **APScheduler** — Background job scheduling
- **Uvicorn** — ASGI server
- **Requests** — Cloud sync HTTP client

## Project Structure
```

The-GateWay-System/
├── app.py               # FastAPI app — main entry point
├── GateWayDetails.py    # Gateway config (ID, location, server URL)
├── database.py          # SQLAlchemy engine and session setup
├── models.py            # DB models: DeviceTable, OTAUpdate
├── storage.py           # Store incoming node data to SQLite
├── read.py              # Read and delete records from SQLite
├── send.py              # Sync buffered data to cloud server
├── send_check.py        # Heartbeat sender
├── OTA_manager.py       # Poll cloud for OTA tasks, download firmware
├── plugin_manager.py    # Dynamic plugin loader
├── template.py          # Pydantic request schema (DeviceBlueprint)
├── plugins/
│   ├── **init**.py
│   └── temperature.py   # Example: LED trigger on high temperature
├── OTA_files/           # Downloaded firmware binaries stored here
└── requirements.txt

```
## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/youruser/The-GateWay-System.git
cd The-GateWay-System
pip install -r requirements.txt
```

### 2. Configure the gateway

Edit `GateWayDetails.py`:

```python
GateWay_ID       = "gateway_001"
GateWay_Location = "home_lab"
server_url       = "https://your-cloud-server.com"
post_auth        = "your_auth_endpoint"
```

### 3. Run the gateway

```bash
uvicorn app:app --host 0.0.0.0 --port 9000
```

The gateway is now reachable at `http://iot-gateway.local:9000` if mDNS is configured, or via its local IP.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/data` | Receive sensor payload from an ESP32 node |
| `GET` | `/ota/{node_id}` | Serve pending firmware to a node |
| `POST` | `/ota/complete/{node_id}` | Mark OTA update as done |

### Incoming data payload (`POST /data`)

```json
{
  "node_id": "sensor_node_1",
  "node_uid": "sensor_uuid_001",
  "node_type": "temperature_sensor",
  "firmware_ver": "1.0",
  "location": "room_1",
  "plugin": "temperature",
  "data": {
    "temperature": 52.3
  }
}
```

## Automation Plugins

Plugins live in the `plugins/` folder and are loaded dynamically based on the `plugin` field in the incoming node payload.

Each plugin must expose a `process(obj)` function.

**Example — `plugins/temperature.py`:**

```python
def process(obj):
    data = dict(obj.data)
    temp = int(data["temperature"])

    if temp > 50:
        # Turn on BeagleBone LEDs as alert
        for led in leds:
            with open(led, "w") as f:
                f.write("1")
```

To add a new plugin:
1. Create `plugins/your_plugin_name.py`
2. Implement `def process(obj):`
3. Set `plugin: "your_plugin_name"` in the node's IoTCore config

## Background Jobs

| Job | Interval | Description |
|---|---|---|
| `sendTOserver()` | Every 15 seconds | Sync buffered SQLite data + send heartbeat to cloud |
| `check_ota()` | Every 30 seconds | Poll cloud for pending OTA firmware tasks |

## OTA Flow

1. Cloud server registers a firmware update for a target node
2. Gateway polls the cloud every 30 seconds via `GET /firmware/{location}/{gateway_id}`
3. Gateway downloads the `.bin` firmware file to `OTA_files/`
4. Gateway stores the OTA task in SQLite with status `pending`
5. Node polls `GET /ota/{node_id}` on the gateway
6. Gateway serves the firmware file and sets status to `in_progress`
7. Node flashes and reboots, then calls `POST /ota/complete/{node_id}`
8. Gateway marks the task `done`

## Local-First Design

The gateway buffers all incoming node data in a local SQLite database (`iot.db`). Data is only deleted from the local buffer after the cloud server confirms successful receipt. This means the system continues recording data even when internet is unavailable.

## Part of The GateWay System

- **[IoTCore]** — ESP32 Arduino library (node firmware)
- **The-GateWay-System** ← You are here
- **[The-Server-System]** — Cloud server (FastAPI + Dashboard)

## License

MIT


