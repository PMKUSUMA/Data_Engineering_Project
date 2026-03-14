import os

# 1. Define the file contents based on your requirements
files = {
    "ingest_data.py": """
import pandas as pd
import numpy as np
import json
import os

def generate_mock_data():
    os.makedirs("data/source_vehicles", exist_ok=True)
    os.makedirs("data/source_dtc", exist_ok=True)

    # Parent Table (The 'One')
    vehicles = {
        "vehicle_id": [f"AV-{i:03d}" for i in range(1, 51)],
        "model": np.random.choice(["Bolt-AV", "Waymo-Gen6", "Zoox-M1"], 50),
        "sw_version": [f"v{np.random.randint(1,5)}.{np.random.randint(0,9)}" for _ in range(50)]
    }
    with open("data/source_vehicles/registry.json", "w") as f:
        json.dump(vehicles, f)

    # Child Table (The 'Many') - 15,000 rows
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
""",
    "transform_data.py": """
import pandas as pd

def merge_data(dtc, vehicles):
    return dtc.merge(vehicles, on="vehicle_id")

def clean_data(df):
    return df.drop_duplicates()

def add_features(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["severity"] = df["dtc_code"].apply(
        lambda x: "High" if x.startswith("P") else "Medium" if x.startswith("C") else "Low"
    )
    return df
""",
    "load_data.py": """
import sqlite3
import os

def load_to_db(df):
    os.makedirs("data/warehouse", exist_ok=True)
    conn = sqlite3.connect("data/warehouse/av_diagnostics.db")
    
    # Create One-to-Many Tables
    df[["vehicle_id", "model", "sw_version"]].drop_duplicates().to_sql(
        "dim_vehicles", conn, if_exists="replace", index=False
    )
    df[["log_id", "vehicle_id", "dtc_code", "timestamp", "severity", "sensor_reading"]].to_sql(
        "fact_diagnostics", conn, if_exists="replace", index=False
    )
    conn.close()
""",
    "run_pipeline.py": """
from ingest_data import generate_mock_data, load_dtc, load_vehicles
from transform_data import merge_data, clean_data, add_features
from load_data import load_to_db

if __name__ == "__main__":
    print("Building environment and generating 15,000 rows...")
    generate_mock_data()
    df = merge_data(load_dtc(), load_vehicles())
    df = add_features(clean_data(df))
    load_to_db(df)
    print("Pipeline complete. Check 'data/warehouse/av_diagnostics.db'")
"""
}

# 2. Write the files to your current directory
for filename, content in files.items():
    with open(filename, "w") as f:
        f.write(content.strip())
    print(f"Created: {filename}")

print("\\nSetup finished! Now run: python run_pipeline.py")