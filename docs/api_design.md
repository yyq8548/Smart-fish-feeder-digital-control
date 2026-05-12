# API Design

## POST /telemetry

Ingests telemetry from a simulated ESP32 device.

Example request:

```json
{
  "temperature_c": 4.6,
  "cooling_on": false,
  "pump_state": "IDLE",
  "event_type": null
}
```

Example response:

```json
{
  "id": 1,
  "temperature_c": 4.6,
  "cooling_on": false,
  "pump_state": "IDLE",
  "event_type": null,
  "alert_level": "normal",
  "alert_message": null,
  "created_at": "2026-07-02T12:00:00Z"
}
```

## GET /telemetry

Returns recent telemetry records for charting.

## GET /device-status

Returns the latest known device status.

## GET /alerts

Returns warning and critical records.