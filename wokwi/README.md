# Wokwi demo
Open this folder as a Wokwi Arduino project. It uses an ESP32, OLED, three LEDs and buzzer, all showing **simulated** readings. Use the Serial Monitor commands: `NORMAL`, `TACHYCARDIA`, `LOW_SPO2`, `HIGH_BP`, `ABNORMAL`, or `EMERGENCY`.

To post to Flask, deploy the Flask app to a URL reachable by Wokwi, set `SERVER_URL` to `https://host/api/reading`, set `API_KEY` to the same value as server `ESP32_API_KEY`, and use a valid app user ID. Wokwi cannot reach a computer's `localhost` directly; use a public tunnel/deployment for the demo.
