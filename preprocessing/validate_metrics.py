import json
from pathlib import Path
from datetime import date

from schemas import Metrics, HistoricalMetrics

DATA_DIR = Path("data")
DAILY_SNAPSHOT_FILE = DATA_DIR / "daily_snapshot.json"
HISTORICAL_METRICS_FILE = DATA_DIR / "historical_metrics.json"

# ----------------------------
# Load historical metrics
# ----------------------------
def load_historical_metrics() -> HistoricalMetrics:
    if not HISTORICAL_METRICS_FILE.exists():
        return HistoricalMetrics()

    try:
        with open(HISTORICAL_METRICS_FILE, "r") as f:
            data = f.read().strip()
            if not data:
                return HistoricalMetrics()
            json_data = json.loads(data)
            if isinstance(json_data, list):
                return HistoricalMetrics(history=[Metrics(**m) for m in json_data])
            elif isinstance(json_data, dict) and "history" in json_data:
                return HistoricalMetrics.model_validate(json_data)
            else:
                print("Warning: historical_metrics.json has unexpected format. Resetting history.")
                return HistoricalMetrics()
    except json.JSONDecodeError:
        print("Warning: historical_metrics.json is invalid. Resetting history.")
        return HistoricalMetrics()

# ----------------------------
# Save historical metrics
# ----------------------------
def save_historical_metrics(historical_metrics: HistoricalMetrics):
    HISTORICAL_METRICS_FILE.parent.mkdir(exist_ok=True)
    with open(HISTORICAL_METRICS_FILE, "w") as f:
        f.write(historical_metrics.model_dump_json(indent=2))

# ----------------------------
# Load daily snapshot
# ----------------------------
def load_daily_snapshot() -> Metrics:
    if not DAILY_SNAPSHOT_FILE.exists():
        # Minimal demo metrics if file is missing
        return Metrics(
            date=date.today(),
            sales=0.0,
            traffic=0,
            inventory={}
        )
    with open(DAILY_SNAPSHOT_FILE, "r") as f:
        snapshot_data = json.load(f)
    metrics_data = snapshot_data.get("metrics", {})
    return Metrics.model_validate(metrics_data)

# ----------------------------
# Validate & process metrics
# ----------------------------
def validate_and_process_metrics():
    metrics = load_daily_snapshot()
    historical_metrics = load_historical_metrics()
    historical_metrics.history.append(metrics)
    save_historical_metrics(historical_metrics)
    return metrics, historical_metrics
