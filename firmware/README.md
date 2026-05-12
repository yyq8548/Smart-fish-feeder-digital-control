# Firmware

Keep your existing Wokwi Arduino firmware here.

Recommended path:

```text
firmware/sketch.ino
```

The v2 backend can work with either:

1. A real ESP32 posting telemetry to `POST /telemetry`
2. A Wokwi simulation concept
3. The included Python mock device client