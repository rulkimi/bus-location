import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from requests import get
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

load_dotenv()

USER_AGENT = os.getenv('EMAIL')

app = FastAPI()

origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class Vehicle(BaseModel):
    vehicle_id: str
    route_id: str
    latitude: float
    longitude: float
    timestamp: int

    def to_dict(self):
        return {
            "vehicle_id": self.vehicle_id,
            "route_id": self.route_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp
        }

# Sample GTFS-R URL from Malaysia's Open API
URL = 'https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-mrtfeeder'

def fetch_gtfs_realtime_feed(url):
    try:
        response = get(url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error fetching GTFS Realtime feed: {e}")
        return None

def reverse_geocode(lat, lon):
    try:
        geolocator = Nominatim(user_agent=USER_AGENT)
        location = geolocator.reverse((lat, lon), exactly_one=True)
        return location.address if location else None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Error: {e}")
        return None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bus Location API"}

@app.get("/routes")
def get_routes():
    feed_content = fetch_gtfs_realtime_feed(URL)
    if not feed_content:
        raise HTTPException(status_code=500, detail="Failed to fetch bus data.")

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(feed_content)
    vehicles = [MessageToDict(entity.vehicle) for entity in feed.entity]

    active_routes = set(vehicle.get('trip', {}).get('routeId', 'N/A') for vehicle in vehicles)

    routes_list = [route for route in active_routes]
    return {"active_routes": routes_list}

@app.get("/vehicle/{route_id}")
def get_vehicle_by_route(route_id: str):
    feed_content = fetch_gtfs_realtime_feed(URL)
    if not feed_content:
        raise HTTPException(status_code=500, detail="Failed to fetch bus data.")

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(feed_content)
    vehicles = [MessageToDict(entity.vehicle) for entity in feed.entity]

    structured_vehicles = []
    for vehicle in vehicles:
        vehicle_id = vehicle.get('vehicle', {}).get('id', 'N/A')
        vehicle_route_id = vehicle.get('trip', {}).get('routeId', 'N/A')
        latitude = vehicle.get('position', {}).get('latitude', 'N/A')
        longitude = vehicle.get('position', {}).get('longitude', 'N/A')
        timestamp = vehicle.get('timestamp', 'N/A')
        structured_vehicle = Vehicle(
            vehicle_id=vehicle_id,
            route_id=vehicle_route_id,
            latitude=latitude,
            longitude=longitude,
            timestamp=timestamp
        )
        structured_vehicles.append(structured_vehicle)

    vehicles_on_route = [vehicle for vehicle in structured_vehicles if vehicle.route_id.lower() == route_id.lower()]

    if not vehicles_on_route:
        raise HTTPException(status_code=404, detail="No bus found for the specified route.")

    result = []
    for vehicle in vehicles_on_route:
        location_name = reverse_geocode(vehicle.latitude, vehicle.longitude)
        result.append({
            "info": vehicle.to_dict(),
            "location": location_name
        })

    return {"vehicles": result}
