# Vitalynx AI
Premium Flask hackathon prototype for simulated pulse, SpO₂, blood-pressure and ECG monitoring. It screens supplied readings with transparent safety rules, saves account-isolated history, offers condition-aware wellness education, and provides an ESP32/Wokwi demonstration path.

## Quick start
```powershell
cd C:\Users\User\Documents\Codex\2026-08-21\files-pasted-by-the-user-build\outputs\pulseguard-ai
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```
Open `http://127.0.0.1:5000`. To test: `pip install pytest` then `pytest -q`.

## Features
- Email/phone login, hashed passwords, session protection, one-time profile onboarding, editable profile
- Six demo modes: Normal, high heart rate, low SpO₂, high BP, abnormal combination, emergency
- Animated six-step health-check UI, ECG demonstration chart, data records and trend graph
- Transparent deterministic health screening, optional AI service boundary, no browser-held keys
- ESP32-protected JSON API and Wokwi visual demo; wellness, reference-range and emergency pages
- Email and phone OTP verification before onboarding, with optional browser location consent during registration
- Development verification codes for offline demos; SMTP and Twilio delivery hooks for production configuration
- Profile-informed food, gentle yoga, and movement education with clear medical-safety boundaries

## Architecture
`simulator or ESP32 → POST /api/reading → SQLite → screening service → dashboard / records`.
The simulator uses the same saving path as the device API. Database tables are `user` and `reading`; every reading is scoped to `user_id`. If `AI_API_KEY` and `AI_MODEL` are configured, the app can use an OpenAI-compatible `/chat/completions` endpoint (change `AI_API_BASE` if needed) only to phrase the already rule-determined safety summary; errors fall back locally.

## Device API
Set `ESP32_API_KEY` in `.env`, then send a JSON request to `POST /api/reading` with header `X-ESP32-API-Key`. Body needs `user_id`, `pulse`, `spo2`, `systolic`, `diastolic`, `heart_rate`, `ecg` (array), and optional `signal_quality`. See [docs/api.md](docs/api.md).

## Wokwi and real hardware
See [wokwi/README.md](wokwi/README.md). The included circuit deliberately labels all sensing as simulated. For real work, use a supported MAX30102 library, an AD8232 analog input with isolation/safety engineering, and an inflatable cuff, pressure sensor, pump, valve and validated oscillometric algorithm for BP. A generic pressure/muscle sensor is not a valid BP measurement.

## Safety
This is a student demonstration and health-monitoring research prototype, **not** a medical device. It does not diagnose illness, prescribe medication, or replace professional care. The ECG waveform is illustrative and not clinically accurate. Seek urgent professional help for severe symptoms.

## HTTPS and transport encryption

The app supports HTTPS enforcement when deployed behind a TLS reverse proxy or a hosting platform that terminates TLS. Configure a valid certificate for your domain at that proxy, then set these values in the deployment environment:

```text
APP_ENV=production
SECRET_KEY=<unique random secret of at least 32 characters>
SESSION_COOKIE_SECURE=true
FORCE_HTTPS=true
ENABLE_HSTS=true
TRUST_PROXY_COUNT=1
```

`TRUST_PROXY_COUNT` must match the number of trusted proxies in front of the app. Set it only when requests can reach the app through that trusted proxy chain; it controls which forwarded HTTPS headers Flask accepts. The app then redirects browser pages to HTTPS, rejects plain-HTTP API calls, marks session cookies `Secure`, and sends HSTS on HTTPS responses. Do not run Flask's development server as the production WSGI server.

For local development, keep `APP_ENV=development`; the local `http://127.0.0.1:5000` workflow remains available. HTTPS transport encryption protects data between the browser/device and the server. The server can still read submitted health data to provide screening, history, and recommendations, so this is not true end-to-end encryption.
