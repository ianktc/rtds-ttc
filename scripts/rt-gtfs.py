import sys
import requests
import sqlite3
from pathlib import Path
from google.transit import gtfs_realtime_pb2
import time
from datetime import datetime, timedelta

def parse_feed(feed):
    vehicle_positions = []
    for entity in feed.entity:
        if entity.HasField('vehicle'):
            vehicle = entity.vehicle
            vehicle_positions.append({
                'vehicle_id': vehicle.vehicle.id,
                'trip_id': vehicle.trip.trip_id,
                'route_id': vehicle.trip.route_id,
                'schedule_relationship': vehicle.trip.schedule_relationship,
                'latitude': round(vehicle.position.latitude, 6),
                'longitude': round(vehicle.position.longitude, 6),
                'bearing': vehicle.position.bearing,
                'speed': round(vehicle.position.speed, 2),
                'timestamp': vehicle.timestamp,
                'occupancy_status': str(vehicle.occupancy_status)
            })
    return vehicle_positions

def insert_trips_table(cursor, record):
    cursor.execute('''
    INSERT OR IGNORE INTO trips (
        trip_id, route_id, timestamp, schedule_relationship, vehicle_id
    ) VALUES (?, ?, ?, ?, ?)
    ''', (
        record['trip_id'], record['route_id'], 
        record['timestamp'], record['schedule_relationship'], 
        record['vehicle_id']
    ))

def insert_vehicle_positions_table(cursor, record):
    cursor.execute('''
    INSERT INTO vehicle_positions (
        vehicle_id, timestamp, latitude, 
        longitude, bearing, speed, occupancy_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        record['vehicle_id'], record['timestamp'], record['latitude'], 
        record['longitude'], record['bearing'], record['speed'], 
        record['occupancy_status']
    ))

def main(sample_period, sample_rate):
    # Set duration and interval
    duration = timedelta(hours=int(sample_period))
    end_time = datetime.now() + duration

    root = Path(__file__).resolve().parents[1]
    db_path = Path(root, 'rtds-ttc.db') 
    print(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    while datetime.now() < end_time:
        
        loop_start = time.time()
        
        try:
            # Fetch GTFS-RT feed
            response = requests.get('https://bustime.ttc.ca/gtfsrt/vehicles')
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)

            vehicle_positions = parse_feed(feed)
            print(f"[{datetime.now()}] Fetched {len(vehicle_positions)} vehicles")

            required_keys = ['route_id', 'trip_id', 'schedule_relationship']

            for record in vehicle_positions:
                valid_trip_record = all(record.get(key) not in ('', None) for key in required_keys)
                if(valid_trip_record):
                    insert_trips_table(cursor, record)
                insert_vehicle_positions_table(cursor, record)
                conn.commit()

        except Exception as e:
            print(f"Error at {datetime.now()}: {e}")

        # Calculate elapsed time and sleep for the remaining interval
        elapsed = time.time() - loop_start
        sleep_time = max(0, int(sample_rate) - elapsed)
        time.sleep(sleep_time)

    conn.commit()
    conn.close()

if __name__=="__main__":
    if len(sys.argv) < 2:
        print("Usage: python rt-gtfs.py <sample_period (h)> <sample_rate (s)>")
        sample_period = 1
        sample_rate = 10
    else:
        sample_period = sys.argv[1]
        sample_rate = sys.argv[2]
    
    main(sample_period, sample_rate)
