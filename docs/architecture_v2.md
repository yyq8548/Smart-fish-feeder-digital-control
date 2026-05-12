# Smart Fish Feeder Digital Twin v2 Architecture

```text
Wokwi Arduino Simulation / Mock ESP32 Client
                |
                | POST /telemetry
                v
        FastAPI Backend
                |
                | SQLAlchemy ORM
                v
          SQLite Database
                |
                | GET /device-status
                | GET /telemetry
                | GET /alerts
                v
          Web Dashboard
```

## Why this is more SDE-oriented

This v2 upgrade turns the original embedded hardware project into a full software system:

- API design
- Data ingestion
- Database persistence
- Telemetry pipeline
- Rule-based alerting
- Frontend dashboard integration
- Local development workflow