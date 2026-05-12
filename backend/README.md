# Backend API

FastAPI backend for Smart Fish Feeder Digital Twin v2.

## Run

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

## Main Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/telemetry` | Ingest telemetry from mock ESP32 client |
| GET | `/telemetry` | Return recent telemetry records |
| GET | `/device-status` | Return latest device status |
| GET | `/alerts` | Return abnormal temperature or pump alerts |

## SQLite Database

The backend automatically creates:

```text
backend/fish_feeder.db
```

Do not commit the database file to GitHub.