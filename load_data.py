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