const API_BASE = "http://127.0.0.1:8000";

const temperatureEl = document.getElementById("temperature");
const coolingStatusEl = document.getElementById("coolingStatus");
const pumpStatusEl = document.getElementById("pumpStatus");
const lastSeenEl = document.getElementById("lastSeen");
const systemHealthEl = document.getElementById("systemHealth");
const alertLogEl = document.getElementById("alertLog");

const ctx = document.getElementById("tempChart");
const chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Reservoir Temperature (°C)",
        data: [],
        tension: 0.35
      }
    ]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        suggestedMin: 2,
        suggestedMax: 7
      }
    }
  }
});

function formatTime(value) {
  if (!value) return "--";
  return new Date(value).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit"
  });
}

function setHealth(level, message) {
  systemHealthEl.textContent = message || level;

  if (level === "critical") {
    systemHealthEl.style.background = "#fde8e8";
    systemHealthEl.style.color = "#9b1c1c";
  } else if (level === "warning") {
    systemHealthEl.style.background = "#fff6e5";
    systemHealthEl.style.color = "#9a6300";
  } else if (level === "normal") {
    systemHealthEl.style.background = "#e8f6ee";
    systemHealthEl.style.color = "#1f7a43";
  } else {
    systemHealthEl.style.background = "#f4f4f5";
    systemHealthEl.style.color = "#3f4652";
  }
}

async function fetchStatus() {
  const response = await fetch(`${API_BASE}/device-status`);
  if (!response.ok) throw new Error("Failed to fetch device status");
  return response.json();
}

async function fetchTelemetry() {
  const response = await fetch(`${API_BASE}/telemetry?limit=30`);
  if (!response.ok) throw new Error("Failed to fetch telemetry");
  return response.json();
}

async function fetchAlerts() {
  const response = await fetch(`${API_BASE}/alerts?limit=8`);
  if (!response.ok) throw new Error("Failed to fetch alerts");
  return response.json();
}

async function refreshDashboard() {
  try {
    const [status, telemetry, alerts] = await Promise.all([
      fetchStatus(),
      fetchTelemetry(),
      fetchAlerts()
    ]);

    if (status.temperature_c === null) {
      temperatureEl.textContent = "--";
      coolingStatusEl.textContent = "--";
      pumpStatusEl.textContent = "--";
      lastSeenEl.textContent = "--";
      setHealth("unknown", "Waiting for telemetry");
    } else {
      temperatureEl.textContent = Number(status.temperature_c).toFixed(1);
      coolingStatusEl.textContent = status.cooling_on ? "ON" : "OFF";
      pumpStatusEl.textContent = status.pump_state;
      lastSeenEl.textContent = formatTime(status.last_seen);
      setHealth(status.alert_level, status.alert_message || "System Normal");
    }

    chart.data.labels = telemetry.map((item) => formatTime(item.created_at));
    chart.data.datasets[0].data = telemetry.map((item) => item.temperature_c);
    chart.update();

    alertLogEl.innerHTML = "";

    if (alerts.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No alerts yet.";
      alertLogEl.appendChild(li);
    } else {
      for (const alert of alerts) {
        const li = document.createElement("li");
        li.textContent = `[${formatTime(alert.created_at)}] ${alert.alert_level.toUpperCase()}: ${alert.alert_message}`;
        alertLogEl.appendChild(li);
      }
    }
  } catch (error) {
    setHealth("unknown", "API Offline");
    console.error(error);
  }
}

refreshDashboard();
setInterval(refreshDashboard, 2000);