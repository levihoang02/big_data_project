DO $$
BEGIN
    -- Create user if not exists
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'iot_user') THEN
        CREATE USER iot_user WITH ENCRYPTED PASSWORD 'iot_password';
    END IF;
END
$$;

-- Create database if not exists
SELECT 'CREATE DATABASE iot_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'iot_db');

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE iot_db TO iot_user;

-- Connect to the iot_db
\c iot_db;

-- Create tables
CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_type VARCHAR(50) NOT NULL,
    value FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_sensor_timestamp ON sensor_readings(timestamp);
CREATE INDEX IF NOT EXISTS idx_sensor_type ON sensor_readings(sensor_type);