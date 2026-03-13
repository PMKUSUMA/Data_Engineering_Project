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
    
    # Business Objectives Analysis
    print("\nBusiness Objectives Analysis:")
    
    # Objective 1: Average DTCs per vehicle
    avg_dtcs = df.groupby('vehicle_id').size().mean()
    print(f"1. Average number of DTCs per vehicle: {avg_dtcs:.2f}")
    
    # Objective 2: Most common DTC code
    most_common_dtc = df['dtc_code'].value_counts().idxmax()
    print(f"2. Most common DTC code: {most_common_dtc}")
    
    # Objective 3: Top vehicles with highest DTC counts
    top_vehicles = df.groupby('vehicle_id').size().nlargest(5)
    print("3. Top 5 vehicles by DTC count:")
    for vid, count in top_vehicles.items():
        print(f"   {vid}: {count} DTCs")