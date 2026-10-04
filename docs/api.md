# ESP32 API
`POST /api/reading` requires `Content-Type: application/json` and `X-ESP32-API-Key` equal to `ESP32_API_KEY`.
```json
{"user_id":1,"pulse":78,"spo2":98,"systolic":120,"diastolic":78,"heart_rate":78,"ecg":[0.0,0.1,0.8,-0.2],"signal_quality":"good"}
```
It returns HTTP 201 with the reading ID and prototype screening summary. Store device keys outside source control and use HTTPS in deployment.


The dashboard displays only readings received through this authenticated device endpoint. A device is considered connected while its last reading is less than two minutes old; after that, live vitals are hidden until another reading arrives. Simulator-generated readings are stored separately and are never shown as live device data. The Wokwi sketch posts every 10 seconds, but its sensor values are simulated.
