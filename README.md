# Smart Fish Feeder Digital Twin v2

A software-oriented upgrade of an Arduino-based automated liquid fish-feeder system.

The original project used:

- DS18B20 temperature sensor
- DS1307 RTC module
- L293D motor driver
- Peristaltic pump
- MOSFET-driven Peltier cooling
- Reverse-pump cleaning logic
- Wokwi simulation

The v2 upgrade adds:

- FastAPI backend
- SQLite database
- SQLAlchemy persistence layer
- Mock ESP32 telemetry client
- Web dashboard consuming real API data
- Rule-based alerts for abnormal temperature and pump errors

---

## System Architecture

```text
Mock ESP32 Client / Wokwi Simulation
              |
              | POST /telemetry
              v
        FastAPI Backend
              |
              v
        SQLite Database
              |
              v
        Web Dashboard
```

---

## Project Structure

```text
smart_fish_feeder_digital_twin_v2/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── mock_device/
│   ├── mock_esp32_client.py
│   ├── requirements.txt
│   └── README.md
├── dashboard/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── README.md
├── docs/
│   ├── architecture_v2.md
│   ├── api_design.md
│   └── resume_bullets.md
├── firmware/
│   └── README.md
├── simulation/
│   └── README.md
└── .gitignore
```

---

## Quick Start on Windows PowerShell

### 1. Start the backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### 2. Start the mock ESP32 client

Open a second PowerShell window:

```powershell
cd mock_device
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python mock_esp32_client.py
```

### 3. Open the dashboard

Open this file in your browser:

```text
dashboard/index.html
```

The dashboard will fetch data from:

```text
http://127.0.0.1:8000
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/telemetry` | Ingest simulated device telemetry |
| GET | `/telemetry` | Return recent telemetry history |
| GET | `/device-status` | Return latest device status |
| GET | `/alerts` | Return warning and critical alerts |

---

## Example Telemetry Payload

```json
{
  "temperature_c": 4.6,
  "cooling_on": false,
  "pump_state": "IDLE",
  "event_type": null
}
```

---

## Resume Bullets

```text
Smart Fish Feeder Digital Twin | Personal Project
Atlanta, GA | Apr 2023 – Jan 2024

- Reconstructed an Arduino-based liquid fish-feeder as a Wokwi simulation with modular firmware for temperature monitoring, RTC-based scheduled dosing, Peltier cooling, and reverse-pump cleaning.
- Built a FastAPI backend with SQLite and SQLAlchemy to ingest simulated ESP32 telemetry, persist temperature and feeding logs, and expose device-status APIs.
- Developed a web dashboard that consumes live API data to visualize reservoir temperature, pump state, feeding events, and rule-based alerts.
```

---

## Future Improvements

- Replace mock client with a real ESP32 Wi-Fi client
- Add authentication for device telemetry ingestion
- Add WebSocket support for real-time dashboard updates
- Deploy backend with Docker
- Add PostgreSQL for production deployment