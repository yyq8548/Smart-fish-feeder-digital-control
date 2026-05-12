# Mock ESP32 Client

This script simulates an ESP32 sending device telemetry to the FastAPI backend.

## Run

Make sure the backend is already running:

```bash
cd backend
uvicorn main:app --reload
```

Then open another terminal:

```bash
cd mock_device
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python mock_esp32_client.py
```

It sends telemetry every 2 seconds:

```json
{
  "temperature_c": 4.6,
  "cooling_on": false,
  "pump_state": "IDLE",
  "event_type": null
}
```