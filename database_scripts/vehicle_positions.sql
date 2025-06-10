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