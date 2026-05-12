# Dashboard

This dashboard fetches real data from the FastAPI backend.

## Run

Start the backend first:

```bash
cd backend
uvicorn main:app --reload
```

Start the mock device in another terminal:

```bash
cd mock_device
python mock_esp32_client.py
```

Then open:

```text
dashboard/index.html
```

The dashboard reads:

- `GET /device-status`
- `GET /telemetry`
- `GET /alerts`