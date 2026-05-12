from datetime import datetime, timezone
from typing import List, Optional

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, create_engine, desc
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fish_feeder.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TelemetryRecord(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    temperature_c = Column(Float, nullable=False)
    cooling_on = Column(Boolean, nullable=False)
    pump_state = Column(String, nullable=False)
    event_type = Column(String, nullable=True)
    alert_level = Column(String, nullable=False, default="normal")
    alert_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class TelemetryIn(BaseModel):
    temperature_c: float = Field(..., description="Reservoir temperature in Celsius")
    cooling_on: bool = Field(..., description="Whether Peltier cooling is active")
    pump_state: str = Field(..., description="IDLE, FEEDING, CLEANING, or ERROR")
    event_type: Optional[str] = Field(default=None, description="Optional event label")


class TelemetryOut(BaseModel):
    id: int
    temperature_c: float
    cooling_on: bool
    pump_state: str
    event_type: Optional[str]
    alert_level: str
    alert_message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DeviceStatus(BaseModel):
    temperature_c: Optional[float]
    cooling_on: Optional[bool]
    pump_state: Optional[str]
    alert_level: str
    alert_message: Optional[str]
    last_event_type: Optional[str]
    last_seen: Optional[datetime]


app = FastAPI(
    title="Smart Fish Feeder Digital Twin API",
    description="Backend API for ingesting simulated ESP32 telemetry and serving feeder status to a dashboard.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_alert(temperature_c: float, pump_state: str) -> tuple[str, Optional[str]]:
    if pump_state.upper() == "ERROR":
        return "critical", "Pump reported an error state."

    if temperature_c >= 6.0:
        return "critical", "Reservoir temperature is dangerously high."

    if temperature_c > 5.0:
        return "warning", "Reservoir temperature is above target range."

    if temperature_c < 2.5:
        return "warning", "Reservoir temperature is below target range."

    return "normal", None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "service": "Smart Fish Feeder Digital Twin API",
        "version": "2.0.0",
        "docs": "/docs",
    }


@app.post("/telemetry", response_model=TelemetryOut)
def ingest_telemetry(payload: TelemetryIn, db: Session = Depends(get_db)):
    alert_level, alert_message = create_alert(payload.temperature_c, payload.pump_state)

    record = TelemetryRecord(
        temperature_c=payload.temperature_c,
        cooling_on=payload.cooling_on,
        pump_state=payload.pump_state.upper(),
        event_type=payload.event_type,
        alert_level=alert_level,
        alert_message=alert_message,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.get("/telemetry", response_model=List[TelemetryOut])
def list_telemetry(limit: int = 50, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 500))

    records = (
        db.query(TelemetryRecord)
        .order_by(desc(TelemetryRecord.created_at))
        .limit(limit)
        .all()
    )

    return list(reversed(records))


@app.get("/device-status", response_model=DeviceStatus)
def get_device_status(db: Session = Depends(get_db)):
    latest = (
        db.query(TelemetryRecord)
        .order_by(desc(TelemetryRecord.created_at))
        .first()
    )

    if latest is None:
        return DeviceStatus(
            temperature_c=None,
            cooling_on=None,
            pump_state=None,
            alert_level="unknown",
            alert_message="No telemetry has been received yet.",
            last_event_type=None,
            last_seen=None,
        )

    return DeviceStatus(
        temperature_c=latest.temperature_c,
        cooling_on=latest.cooling_on,
        pump_state=latest.pump_state,
        alert_level=latest.alert_level,
        alert_message=latest.alert_message,
        last_event_type=latest.event_type,
        last_seen=latest.created_at,
    )


@app.get("/alerts", response_model=List[TelemetryOut])
def list_alerts(limit: int = 20, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 100))

    records = (
        db.query(TelemetryRecord)
        .filter(TelemetryRecord.alert_level != "normal")
        .order_by(desc(TelemetryRecord.created_at))
        .limit(limit)
        .all()
    )

    return records