


# The-GateWay-System

An **IoT Gateway System** designed to simulate how industrial IoT infrastructures manage and forward sensor data.

This project acts as a **local gateway between IoT nodes and a central server/cloud**, buffering data locally and forwarding it when connectivity is available.

The goal of this project is to **replicate industrial IoT architecture in small environments** such as homes, labs, or small research setups.



# Architecture Overview

```

ESP32 / Arduino / STM32 Nodes
│
│ HTTP JSON
▼
IoT Gateway (FastAPI)
(Local Buffer + Scheduler)
│
│ Forwarding
▼
Central Server (Raspberry Pi / Cloud / AWS)
│
▼
Permanent Database + Dashboard

````

---

# Node Layer

IoT nodes are microcontrollers such as:

- ESP32
- Arduino
- STM32

These devices send **JSON sensor data via HTTP** to the gateway.

Example packet format:

```json
{
  "node_id": "test_node_01",
  "data": {
    "temperature": 25,
    "humidity": 60,
    "voltage": 3.3
  }
}
````

---

# Gateway Layer

The **Gateway** acts as an intermediate system between nodes and the central server.

Responsibilities:

* Receive node data
* Validate JSON payload
* Store data locally
* Forward data to the server periodically
* Prevent data loss when internet connectivity is unavailable

Gateway software can run on:

* Raspberry Pi
* BeagleBone
* Edge devices
* Mini PCs
* Local servers

The gateway exposes an endpoint:

```
POST /data
```

---

# Local Data Buffer

The gateway stores incoming node data in a **local SQLite database**.

This ensures:

* No data loss if the server is offline
* Reliable forwarding
* Temporary local storage

Stored fields include:

* node_id
* timestamp
* sensor payload

---

# Store and Forward System

A background scheduler periodically checks the server connectivity and forwards stored packets.

Workflow:

1. Node sends data
2. Gateway stores it locally
3. Scheduler checks server connectivity
4. If server is reachable:

   * Send stored data
   * Delete successfully transmitted entries

---

# Features

### Current Features

* FastAPI-based gateway
* JSON data ingestion
* Local SQLite buffering
* Scheduled server forwarding
* Modular storage system
* Pydantic validation for packets

### Planned Features

* OTA firmware updates for nodes
* Plugin system for device types
* Local web dashboard
* Node authentication
* Edge analytics

---

# Gateway Configuration

Gateway parameters are configured in:

```
GateWayDetails.py
```

Example:

```python
GateWay_ID=""
GateWay_Location=""
server_url=""
post_auth=""
```

These values allow the gateway to identify itself when communicating with the central server.

---

# Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/The-GateWay-System.git
cd The-GateWay-System
```

Create virtual environment

```bash
python -m venv env
```

Activate environment

Linux / Mac

```bash
source env/bin/activate
```

Windows

```bash
env\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Gateway

Start the gateway server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Gateway endpoint

```
http://<gateway-ip>:8000/data
```

---

# ESP32 Test Node

Use this ESP32 code to test communication with the gateway.

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "Utkarsha-2.4G";
const char* password = "YOUR_WIFI_PASSWORD";

const char* gateway_url = "http://192.168.1.5:8000/data";

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
}

void loop() {

  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;
    http.begin(gateway_url);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> doc;

    doc["node_id"] = "test_node_01";

    JsonObject data = doc.createNestedObject("data");

    data["temperature"] = random(20, 35);
    data["humidity"] = random(40, 80);
    data["voltage"] = random(3, 5);

    String json;
    serializeJson(doc, json);

    Serial.println("Sending:");
    Serial.println(json);

    int httpResponseCode = http.POST(json);

    Serial.print("Response: ");
    Serial.println(httpResponseCode);

    http.end();
  }

  delay(30000);
}
```

---

# Project Status

This project is currently **under active development**.

Upcoming components include:

* Plugin architecture
* Node OTA system
* Gateway UI
* Advanced node management

---

# Purpose of the Project

The aim of this project is to **learn and replicate real-world IoT infrastructure concepts**, including:

* Edge computing
* Gateway-based architectures
* Store-and-forward reliability
* Device management systems


