import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Database path
DB_PATH = "data/warehouse/av_diagnostics.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def run_query(query):
    conn = get_db_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def execute_query(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()

# Business Queries
QUERIES = {
    "Average DTCs per Vehicle": """
        SELECT AVG(dtc_count) as avg_dtcs_per_vehicle
        FROM (
            SELECT vehicle_id, COUNT(*) as dtc_count
            FROM fact_diagnostics
            GROUP BY vehicle_id
        )
    """,
    "Top 5 Vehicles by DTC Count": """
        SELECT v.vehicle_id, v.model, COUNT(f.log_id) as dtc_count
        FROM dim_vehicles v
        JOIN fact_diagnostics f ON v.vehicle_id = f.vehicle_id
        GROUP BY v.vehicle_id, v.model
        ORDER BY dtc_count DESC
        LIMIT 5
    """,
    "Most Common DTC Codes": """
        SELECT dtc_code, COUNT(*) as frequency
        FROM fact_diagnostics
        GROUP BY dtc_code
        ORDER BY frequency DESC
        LIMIT 10
    """,
    "DTC Severity Distribution": """
        SELECT severity, COUNT(*) as count
        FROM fact_diagnostics
        GROUP BY severity
        ORDER BY count DESC
    """,
    "DTC Counts by Model": """
        SELECT v.model, COUNT(f.log_id) as total_dtcs, COUNT(DISTINCT v.vehicle_id) as vehicle_count,
               ROUND(CAST(COUNT(f.log_id) AS FLOAT) / COUNT(DISTINCT v.vehicle_id), 2) as avg_dtcs_per_model
        FROM dim_vehicles v
        LEFT JOIN fact_diagnostics f ON v.vehicle_id = f.vehicle_id
        GROUP BY v.model
        ORDER BY total_dtcs DESC
    """,
    "DTC by Software Version": """
        SELECT v.sw_version, COUNT(f.log_id) as dtc_count
        FROM dim_vehicles v
        JOIN fact_diagnostics f ON v.vehicle_id = f.vehicle_id
        GROUP BY v.sw_version
        ORDER BY dtc_count DESC
    """,
    "Sensor Readings by DTC": """
        SELECT dtc_code, AVG(sensor_reading) as avg_sensor_reading, COUNT(*) as occurrences
        FROM fact_diagnostics
        GROUP BY dtc_code
        ORDER BY occurrences DESC
        LIMIT 10
    """
}

def main():
    st.title("🚗 AV Diagnostics Dashboard")
    st.markdown("Business Intelligence for Autonomous Vehicle Fleet Management")

    # Sidebar for navigation
    page = st.sidebar.selectbox("Select Analysis", ["Overview", "Maintenance", "Performance", "Software Analysis", "Add Data"])

    if page == "Overview":
        st.header("📊 Overview Dashboard")

        col1, col2 = st.columns(2)

        with col1:
            # Average DTCs
            avg_df = run_query(QUERIES["Average DTCs per Vehicle"])
            st.metric("Average DTCs per Vehicle", f"{avg_df.iloc[0,0]:.1f}")

            # Total DTCs
            total_df = run_query("SELECT COUNT(*) as total FROM fact_diagnostics")
            st.metric("Total DTC Records", f"{total_df.iloc[0,0]:,}")

        with col2:
            # Total Vehicles
            vehicles_df = run_query("SELECT COUNT(*) as total FROM dim_vehicles")
            st.metric("Total Vehicles", f"{vehicles_df.iloc[0,0]:,}")

            # Most Common DTC
            common_df = run_query(QUERIES["Most Common DTC Codes"])
            st.metric("Most Common DTC", common_df.iloc[0,0])

        # Severity Distribution Chart
        st.subheader("DTC Severity Distribution")
        severity_df = run_query(QUERIES["DTC Severity Distribution"])
        fig = px.pie(severity_df, values='count', names='severity', title="DTC Severity Levels")
        st.plotly_chart(fig)

    elif page == "Maintenance":
        st.header("🔧 Maintenance Prioritization")

        # Top vehicles chart
        st.subheader("Top 5 Vehicles by DTC Count")
        top_df = run_query(QUERIES["Top 5 Vehicles by DTC Count"])
        fig = px.bar(top_df, x='vehicle_id', y='dtc_count', color='model', title="Vehicles with Highest DTC Counts")
        st.plotly_chart(fig)

        st.dataframe(top_df)

        # DTC frequency
        st.subheader("Most Common DTC Codes")
        dtc_df = run_query(QUERIES["Most Common DTC Codes"])
        fig2 = px.bar(dtc_df, x='dtc_code', y='frequency', title="DTC Code Frequency")
        st.plotly_chart(fig2)

    elif page == "Performance":
        st.header("📈 Performance Monitoring")

        # Model performance
        st.subheader("DTC Counts by Vehicle Model")
        model_df = run_query(QUERIES["DTC Counts by Model"])
        fig = px.bar(model_df, x='model', y='total_dtcs', title="Total DTCs by Model")
        st.plotly_chart(fig)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Best Performing Model", model_df.iloc[-1]['model'])
        with col2:
            st.metric("Worst Performing Model", model_df.iloc[0]['model'])

        st.dataframe(model_df)

    elif page == "Software Analysis":
        st.header("💻 Software Version Analysis")

        # Software version DTCs
        st.subheader("DTC Counts by Software Version")
        sw_df = run_query(QUERIES["DTC by Software Version"])
        fig = px.bar(sw_df, x='sw_version', y='dtc_count', title="DTCs by Software Version")
        st.plotly_chart(fig)

        st.dataframe(sw_df)

        # Sensor analysis
        st.subheader("Sensor Readings Analysis")
        sensor_df = run_query(QUERIES["Sensor Readings by DTC"])
        fig2 = px.scatter(sensor_df, x='dtc_code', y='avg_sensor_reading', size='occurrences',
                         title="Average Sensor Readings by DTC Code")
        st.plotly_chart(fig2)

    elif page == "Add Data":
        st.header("➕ Add New Diagnostic Data")

        with st.form("add_dtc_form"):
            st.subheader("Add New DTC Record")

            vehicle_id = st.selectbox("Vehicle ID", run_query("SELECT vehicle_id FROM dim_vehicles")['vehicle_id'].tolist())
            dtc_code = st.text_input("DTC Code", "P0001")
            timestamp = st.date_input("Date", datetime.now().date())
            time_input = st.time_input("Time", datetime.now().time())
            timestamp_full = datetime.combine(timestamp, time_input)
            severity = st.selectbox("Severity", ["High", "Medium", "Low"])
            sensor_reading = st.number_input("Sensor Reading", 0.0, 100.0, 50.0)

            submitted = st.form_submit_button("Add Record")

            if submitted:
                try:
                    # Get next log_id
                    max_id_df = run_query("SELECT MAX(log_id) as max_id FROM fact_diagnostics")
                    next_id = (max_id_df.iloc[0,0] or 0) + 1

                    execute_query("""
                        INSERT INTO fact_diagnostics (log_id, vehicle_id, dtc_code, timestamp, severity, sensor_reading)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (next_id, vehicle_id, dtc_code, timestamp_full.isoformat(), severity, sensor_reading))

                    st.success("✅ Record added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error adding record: {e}")

        # Add new vehicle
        with st.form("add_vehicle_form"):
            st.subheader("Add New Vehicle")

            new_vehicle_id = st.text_input("Vehicle ID", "AV-051")
            model = st.selectbox("Model", ["Bolt-AV", "Waymo-Gen6", "Zoox-M1"])
            sw_version = st.text_input("Software Version", "v1.0")

            submitted_vehicle = st.form_submit_button("Add Vehicle")

            if submitted_vehicle:
                try:
                    execute_query("""
                        INSERT INTO dim_vehicles (vehicle_id, model, sw_version)
                        VALUES (?, ?, ?)
                    """, (new_vehicle_id, model, sw_version))

                    st.success("✅ Vehicle added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error adding vehicle: {e}")

if __name__ == "__main__":
    main()