The-GateWay-SystemAn intermediate IoT Gateway designed to bridge local sensor nodes (ESP32, Arduino, STM32) with a central cloud or local server (Raspberry Pi/AWS). This system ensures data reliability by storing sensor packets locally in a SQLite database and forwarding them to the main server only when an active internet connection is detected.## Key FeaturesLocal Data Persistence: Uses SQLAlchemy and SQLite to queue data locally if the server is offline. Asynchronous Scheduling: Implements APScheduler to periodically check server health and sync pending data. Edge Processing: Acts as a buffer between low-power microcontrollers and heavy cloud infrastructures.Lightweight API: Built with FastAPI for high-performance data reception from local nodes. ## System ArchitectureNodes: Sensors send JSON data via HTTP POST to the Gateway.Gateway: Receives data, logs it into iot.db, and runs a background job every 15 seconds to sync with the server.Server: Receives consolidated packets and stores them permanently.## Getting Started1. ConfigurationUpdate GateWayDetails.py with your specific environment details:PythonGateWay_ID = "GW-001"
GateWay_Location = "Lab-1"
server_url = "http://your-server-ip:5000"
post_auth = "upload-endpoint"
2. InstallationBashpip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
## Testing with ESP32Use the following Arduino sketch to simulate a node sending temperature, humidity, and voltage data to your gateway.C++#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* gateway_url = "http://<GATEWAY_IP>:8000/data";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
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
    int httpResponseCode = http.POST(json);
    
    Serial.println("Sent: " + json);
    Serial.println("Response: " + String(httpResponseCode));
    http.end();
  }
  delay(30000); 
}
## Upcoming RoadmapPlugin System: Specialized handlers for specific nodes (e.g., RFID, Fan Controllers).UI Dashboard: Real-time rendering of node status at the gateway level.OTA Updates: Over-The-Air firmware management for connected microcontrollers.
