import json
from pathlib import Path
from datetime import date

from schemas import Metrics, HistoricalMetrics

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------
DATA_DIR = Path("data")
DAILY_SNAPSHOT_FILE = DATA_DIR / "daily_snapshot.json"
HISTORICAL_METRICS_FILE = DATA_DIR / "historical_metrics.json"

# -------------------------------------------------------------------
# Functions
# -------------------------------------------------------------------
def load_historical_metrics() -> HistoricalMetrics:
    """
    Load historical metrics from the JSON file.
    If file doesn't exist, initialize an empty history.
    """
    if HISTORICAL_METRICS_FILE.exists():
        with open(HISTORICAL_METRICS_FILE, "r") as f:
            historical_data = json.load(f)
        history = [Metrics(**m) for m in historical_data]
        return HistoricalMetrics(history=history)
    else:
        return HistoricalMetrics(history=[])


def save_historical_metrics(historical_metrics: HistoricalMetrics):
    """
    Save the historical metrics back to disk.
    """
    HISTORICAL_METRICS_FILE.parent.mkdir(exist_ok=True)
    with open(HISTORICAL_METRICS_FILE, "w") as f:
        json.dump([m.dict() for m in historical_metrics.history], f, indent=2)


def load_daily_snapshot() -> Metrics:
    """
    Load and validate today's metrics from daily_snapshot.json.
    """
    with open(DAILY_SNAPSHOT_FILE, "r") as f:
        snapshot_data = json.load(f)

    metrics_data = snapshot_data.get("metrics", {})
    metrics = Metrics(**metrics_data)
    return metrics


def validate_and_process_metrics():
    """
    Main function to load, validate, and update metrics.
    Returns:
      - metrics: Metrics for today
      - historical_metrics: HistoricalMetrics including today's validated metrics
    """
    # Load today's metrics
    metrics = load_daily_snapshot()

    # Load historical metrics
    historical_metrics = load_historical_metrics()

    # Append today's metrics
    historical_metrics.history.append(metrics)

    # Save updated historical metrics back to file
    save_historical_metrics(historical_metrics)

    return metrics, historical_metrics


# -------------------------------------------------------------------
# Test run (optional)
# -------------------------------------------------------------------
if __name__ == "__main__":
    m, h = validate_and_process_metrics()
    print("Today's metrics validated:", m)
    print(f"Historical metrics count: {len(h.history)}")
