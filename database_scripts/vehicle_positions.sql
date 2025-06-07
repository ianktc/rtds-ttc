CREATE TABLE vehicle_positions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  vehicle_id TEXT,
  trip_id TEXT,
  route_id TEXT,
  timestamp INTEGER,
  latitude REAL,
  longitude REAL,
  bearing REAL,
  speed REAL,
  occupancy_status TEXT
);