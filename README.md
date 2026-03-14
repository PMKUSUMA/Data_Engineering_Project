# Data Engineering Project

## Overview
This project implements a data engineering pipeline for processing and analyzing vehicle diagnostic trouble codes (DTC) and sensor data from autonomous vehicles (AVs). The pipeline ingests data from multiple sources, performs data transformation and cleaning, adds analytical features, and loads the processed data into a SQLite database for further analysis.

## Description
The pipeline consists of four main components:
- **Data Ingestion**: Loads DTC logs from CSV files and vehicle registry data from JSON files
- **Data Transformation**: Merges datasets, cleans missing values, and adds computed features
- **Feature Engineering**: Calculates additional metrics like failure rates and diagnostic insights
- **Data Loading**: Stores the processed data in an SQLite database for querying and analysis

The project generates synthetic data (15,000 rows) to simulate real-world AV diagnostic scenarios, making it suitable for testing data processing workflows and analytics.

## Prerequisites
- Python 3.7 or higher
- Required Python packages:
  - pandas
  - numpy
## NOTE:
- A Python environment should be configured(virtual python environment should be created)
- 1.Environment type: system
- 2.Version: 3.9.6.final.0

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/PMKUSUMA/Data_Engineering_Project.git
   cd Data_Engineering_Project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the complete data pipeline with the following command:

```bash
python run_pipeline.py
```

### Step-by-Step Execution:
1. **Data Generation**: The pipeline generates 15,000 rows of synthetic AV diagnostic data
2. **Data Ingestion**: Loads DTC logs from `data/source_dtc/dtc_logs.csv` and vehicle registry from `data/source_vehicles/registry.json`
3. **Data Merging**: Combines DTC and vehicle data based on vehicle IDs
4. **Data Cleaning**: Removes duplicates, handles missing values, and standardizes data formats
5. **Feature Addition**: Calculates additional metrics such as failure rates and diagnostic patterns
6. **Data Loading**: Stores the processed data in `data/warehouse/av_diagnostics.db`

## Dashboard
Launch the interactive dashboard to visualize business insights and manage data:

```bash
streamlit run dashboard.py
Note: if in python terminal command is python -m streamlit run dashboard.py
```

The dashboard provides:
- **Overview**: Key metrics and severity distribution charts
- **Maintenance**: Vehicle prioritization and DTC frequency analysis
- **Performance**: Model-wise performance monitoring
- **Software Analysis**: Version-specific insights and sensor data visualization
- **Add Data**: Forms to insert new DTC records and vehicles (updates reflected in database)

## Data Sources
- **DTC Logs**: CSV file containing diagnostic trouble codes with timestamps and severity levels
- **Vehicle Registry**: JSON file with vehicle information including model, software version, and registration details

## Business Objectives
This data pipeline fulfills the following business objectives for autonomous vehicle diagnostics:

1. **Maintenance Prioritization**: Identify vehicles with the highest number of diagnostic trouble codes (DTCs) to prioritize maintenance and reduce downtime. Also identifies vehicles with zero DTCs for benchmarking.
2. **Failure Pattern Analysis**: Determine the most common DTC codes, severity distributions, and model-specific failure patterns across the fleet to inform software updates and hardware improvements.
3. **Performance Monitoring**: Calculate average DTC counts per vehicle and by model to monitor overall fleet health and detect trends. Includes monthly and daily trend analysis.
4. **Software Version Analysis**: Analyze DTC frequencies and severity distributions by software version to identify problematic releases.
5. **Sensor Data Insights**: Examine average sensor readings associated with DTC codes, reading ranges by severity, and detect anomalous sensor readings for diagnostic insights.
6. **Temporal Analysis**: Analyze DTC patterns by time of day and compare weekday vs weekend occurrences to understand operational patterns.
7. **Predictive Maintenance**: Identify vehicles showing increasing DTC trends to enable proactive maintenance scheduling.

## Business Queries
The `sql/business_queries.sql` file contains SQL queries that implement these business objectives. To execute the queries:

```bash
python run_queries.py
```

This will run all queries against the SQLite database and display the results, providing actionable insights for AV operations teams.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
