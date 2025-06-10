DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS vehicle_positions;

CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY,
    schedule_relationship TEXT,
    route_id INTEGER,
    vehicle_id INTEGER UNIQUE,
    timestamp INTEGER
);

CREATE TABLE IF NOT EXISTS vehicle_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER,
    latitude REAL,
    longitude REAL,
    occupancy_status TEXT,
    speed REAL,
    bearing REAL,
    timestamp INTEGER,
    FOREIGN KEY (vehicle_id) REFERENCES trips(vehicle_id)
);

CREATE INDEX idx_vehicle_positions_timestamp ON vehicle_positions(timestamp);