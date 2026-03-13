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

-- Query: Vehicles with zero DTCs
SELECT v.vehicle_id, v.model
FROM dim_vehicles v
LEFT JOIN fact_diagnostics f ON v.vehicle_id = f.vehicle_id
GROUP BY v.vehicle_id, v.model
HAVING COUNT(f.log_id) = 0;

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

-- Query: DTC codes by model
SELECT v.model, f.dtc_code, COUNT(*) as frequency
FROM dim_vehicles v
JOIN fact_diagnostics f ON v.vehicle_id = f.vehicle_id
GROUP BY v.model, f.dtc_code
ORDER BY v.model, frequency DESC;

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

-- Query: Monthly DTC trends
SELECT strftime('%Y-%m', timestamp) as month, COUNT(*) as monthly_dtcs
FROM fact_diagnostics
GROUP BY strftime('%Y-%m', timestamp)
ORDER BY month DESC;

-- Business Objective 4: Software Version Analysis
-- Query: DTC counts by software version
SELECT v.sw_version, COUNT(f.log_id) as dtc_count
FROM dim_vehicles v
JOIN fact_diagnostics f ON v.vehicle_id = f.vehicle_id
GROUP BY v.sw_version
ORDER BY dtc_count DESC;

-- Query: Severity distribution by software version
SELECT v.sw_version, f.severity, COUNT(*) as count
FROM dim_vehicles v
JOIN fact_diagnostics f ON v.vehicle_id = f.vehicle_id
GROUP BY v.sw_version, f.severity
ORDER BY v.sw_version, count DESC;

-- Business Objective 5: Sensor Data Insights
-- Query: Average sensor readings by DTC code
SELECT dtc_code, AVG(sensor_reading) as avg_sensor_reading, COUNT(*) as occurrences
FROM fact_diagnostics
GROUP BY dtc_code
ORDER BY occurrences DESC
LIMIT 10;

-- Query: Sensor reading ranges by severity
SELECT severity, MIN(sensor_reading) as min_reading, MAX(sensor_reading) as max_reading,
       AVG(sensor_reading) as avg_reading
FROM fact_diagnostics
GROUP BY severity
ORDER BY avg_reading DESC;

-- Query: Anomalous sensor readings (outside 2 standard deviations)
WITH stats AS (
    SELECT AVG(sensor_reading) as mean, STDEV(sensor_reading) as stddev
    FROM fact_diagnostics
)
SELECT dtc_code, sensor_reading, severity
FROM fact_diagnostics, stats
WHERE sensor_reading < mean - 2*stddev OR sensor_reading > mean + 2*stddev
ORDER BY ABS(sensor_reading - mean) DESC
LIMIT 10;

-- Business Objective 6: Temporal Analysis
-- Query: DTC frequency by hour of day
SELECT strftime('%H', timestamp) as hour, COUNT(*) as dtc_count
FROM fact_diagnostics
GROUP BY strftime('%H', timestamp)
ORDER BY hour;

-- Query: Weekday vs Weekend DTC patterns
SELECT CASE WHEN strftime('%w', timestamp) IN ('0','6') THEN 'Weekend' ELSE 'Weekday' END as day_type,
       COUNT(*) as dtc_count
FROM fact_diagnostics
GROUP BY day_type;

-- Business Objective 7: Predictive Maintenance
-- Query: Vehicles with increasing DTC frequency (last 7 days vs previous 7 days)
WITH recent AS (
    SELECT vehicle_id, COUNT(*) as recent_count
    FROM fact_diagnostics
    WHERE timestamp >= date('now', '-7 days')
    GROUP BY vehicle_id
),
previous AS (
    SELECT vehicle_id, COUNT(*) as prev_count
    FROM fact_diagnostics
    WHERE timestamp BETWEEN date('now', '-14 days') AND date('now', '-7 days')
    GROUP BY vehicle_id
)
SELECT r.vehicle_id, COALESCE(r.recent_count, 0) as recent, COALESCE(p.prev_count, 0) as previous,
       COALESCE(r.recent_count, 0) - COALESCE(p.prev_count, 0) as change
FROM recent r
FULL OUTER JOIN previous p ON r.vehicle_id = p.vehicle_id
WHERE COALESCE(r.recent_count, 0) > COALESCE(p.prev_count, 0)
ORDER BY change DESC;