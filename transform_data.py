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