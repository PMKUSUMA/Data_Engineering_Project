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