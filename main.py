from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import pandas as pd
from requests import get

class Vehicle:
    def __init__(self, vehicle_id, route_id, latitude, longitude, timestamp):
        self.vehicle_id = vehicle_id
        self.route_id = route_id
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp

    def __str__(self):
        return f"Vehicle ID: {self.vehicle_id}, Route ID: {self.route_id}, Latitude: {self.latitude}, Longitude: {self.longitude}, Timestamp: {self.timestamp}"

# Sample GTFS-R URL from Malaysia's Open API
URL = 'https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kl'

# Parse the GTFS Realtime feed
feed = gtfs_realtime_pb2.FeedMessage()
response = get(URL)
feed.ParseFromString(response.content)

# Extract and print vehicle position information
vehicles = [MessageToDict(entity.vehicle) for entity in feed.entity]

structured_vehicles = []
for vehicle in vehicles:
    vehicle_id = vehicle.get('vehicle', {}).get('id', 'N/A')
    route_id = vehicle.get('trip', {}).get('routeId', 'N/A')
    latitude = vehicle.get('position', {}).get('latitude', 'N/A')
    longitude = vehicle.get('position', {}).get('longitude', 'N/A')
    timestamp = vehicle.get('timestamp', 'N/A')
    structured_vehicle = Vehicle(vehicle_id, route_id, latitude, longitude, timestamp)
    structured_vehicles.append(structured_vehicle)

bus_route = input("Which bus to see? ")

for vehicle in structured_vehicles:
    if bus_route.lower() == vehicle.route_id.lower():
        print('Bus found:')
        print(vehicle)
        break
else:
    print('No bus found for the specified route.')
