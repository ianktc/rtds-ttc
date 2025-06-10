CREATE TABLE IF NOT EXISTS trips (
    trip_id INTEGER PRIMARY KEY,
    schedule_relationship TEXT,
    route_id INTEGER,
    vehicle_id INTEGER UNIQUE,
    timestamp INTEGER
);