-- Business Queries for AV Diagnostics Data Engineering Project
-- Database: data/warehouse/av_diagnostics.db
-- Tables: dim_vehicles, fact_diagnostics

-- Business Objective 1: Maintenance Prioritization
-- Query: Average number of DTCs per vehicle
SELECT AVG(dtc_count) as avg_dtcs_per_vehicle
FROM (
    SELECT vehicle_id, COUNT(*) as dtc_count
    FROM fact_diagnostics
    GROUP BY vehicle_id
);

-- Query: Top 5 vehicles with highest DTC counts
SELECT v.vehicle_id, v.model, COUNT(f.log_id) as dtc_count
FROM dim_vehicles v
JOIN fact_diagnostics f ON v.vehicle_id = f.vehicle_id
GROUP BY v.vehicle_id, v.model
ORDER BY dtc_count DESC
LIMIT 5;

-- Business Objective 2: Failure Pattern Analysis
-- Query: Most common DTC codes
SELECT dtc_code, COUNT(*) as frequency
FROM fact_diagnostics
GROUP BY dtc_code
ORDER BY frequency DESC
LIMIT 10;

-- Query: DTC frequency by severity level
SELECT severity, COUNT(*) as count
FROM fact_diagnostics
GROUP BY severity
ORDER BY count DESC;

-- Business Objective 3: Performance Monitoring
-- Query: DTC counts by vehicle model
SELECT v.model, COUNT(f.log_id) as total_dtcs, COUNT(DISTINCT v.vehicle_id) as vehicle_count,
       ROUND(CAST(COUNT(f.log_id) AS FLOAT) / COUNT(DISTINCT v.vehicle_id), 2) as avg_dtcs_per_model
FROM dim_vehicles v
LEFT JOIN fact_diagnostics f ON v.vehicle_id = f.vehicle_id
GROUP BY v.model
ORDER BY total_dtcs DESC;

-- Query: Recent DTC trends (last 30 days - assuming current date)
SELECT DATE(timestamp) as date, COUNT(*) as daily_dtcs
FROM fact_diagnostics
WHERE timestamp >= date('now', '-30 days')
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- Business Objective 4: Software Version Analysis
-- Query: DTC counts by software version
SELECT v.sw_version, COUNT(f.log_id) as dtc_count
FROM dim_vehicles v
JOIN fact_diagnostics f ON v.vehicle_id = f.vehicle_id
GROUP BY v.sw_version
ORDER BY dtc_count DESC;

-- Query: Average sensor readings by DTC code
SELECT dtc_code, AVG(sensor_reading) as avg_sensor_reading, COUNT(*) as occurrences
FROM fact_diagnostics
GROUP BY dtc_code
ORDER BY occurrences DESC
LIMIT 10;