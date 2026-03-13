import pandas as pd
import numpy as np
import json
import os

def generate_mock_data():
    """Generates 15,000 rows of synthetic AV diagnostic data."""
    os.makedirs("data/source_vehicles", exist_ok=True)
    os.makedirs("data/source_dtc", exist_ok=True)

    # Parent Table: Vehicle Registry (The 'One')
    vehicles = {
        "vehicle_id": [f"AV-{i:03d}" for i in range(1, 51)],
        # FIXED: Added .tolist() to make it JSON serializable
        "model": np.random.choice(["Bolt-AV", "Waymo-Gen6", "Zoox-M1"], 50).tolist(),
        "sw_version": [f"v{np.random.randint(1,5)}.{np.random.randint(0,9)}" for _ in range(50)]
    }
    
    with open("data/source_vehicles/registry.json", "w") as f:
        json.dump(vehicles, f, indent=4)

    # Child Table: Diagnostic Logs (The 'Many') - 15,000 rows
    rows = 15000
    dtc_data = {
        "log_id": range(1, rows + 1),
        "vehicle_id": [f"AV-{np.random.randint(1, 51):03d}" for _ in range(rows)],
        "dtc_code": np.random.choice(["P0A1B", "C1201", "U0100", "B1421"], rows),
        "timestamp": pd.date_range(start="2026-01-01", periods=rows, freq="min"),
        "sensor_reading": np.random.uniform(0.1, 100.0, rows)
    }
    pd.DataFrame(dtc_data).to_csv("data/source_dtc/dtc_logs.csv", index=False)

def load_dtc():
    return pd.read_csv("data/source_dtc/dtc_logs.csv")

def load_vehicles():
    return pd.read_json("data/source_vehicles/registry.json")