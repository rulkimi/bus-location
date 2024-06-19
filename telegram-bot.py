from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from requests import get
import os
from dotenv import load_dotenv
import telebot
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

URL = 'https://api.data.gov.my/gtfs-realtime/vehicle-position/prasarana?category=rapid-bus-kl'

# Parse the GTFS Realtime feed
feed = gtfs_realtime_pb2.FeedMessage()
response = get(URL)
feed.ParseFromString(response.content)

class Vehicle:
    def __init__(self, vehicle_id, route_id, latitude, longitude, timestamp):
        self.vehicle_id = vehicle_id
        self.route_id = route_id
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp

    def __str__(self):
        return f"Vehicle ID: {self.vehicle_id}, Route ID: {self.route_id}, Latitude: {self.latitude}, Longitude: {self.longitude}, Timestamp: {self.timestamp}"

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

def reverse_geocode(lat, lon):
  try:
    geolocator = Nominatim(user_agent="geoapiExecisese")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    return location.address if location else None
  except (GeocoderTimedOut, GeocoderServiceError) as e:
    print(f"Error: {e}")
    return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Bus Tracker Bot! Type /track to start tracking a bus route.")

@bot.message_handler(commands=['track'])
def track_command(message):
    bot.reply_to(message, "Please enter the bus route you want to track.")

@bot.message_handler(func=lambda message: True)
def track_bus(message):
    bus_route = message.text.strip().lower()

    for vehicle in structured_vehicles:
        if bus_route == vehicle.route_id.lower():
            # Create a map centered around the bus's location
            location_map = folium.Map(location=[vehicle.latitude, vehicle.longitude], zoom_start=15)
            folium.Marker([vehicle.latitude, vehicle.longitude], popup=f"Bus {vehicle.vehicle_id} - Route {vehicle.route_id}").add_to(location_map)
            
            location_name = reverse_geocode(vehicle.latitude, vehicle.longitude)
            # Send the location as a location pin
            bot.send_location(message.chat.id, vehicle.latitude, vehicle.longitude)
            bot.send_message(message.chat.id, f"Bus found at {location_name}\n{vehicle}")
            return
    
    bot.send_message(message.chat.id, 'No bus found for the specified route.')

# Start the bot
bot.polling()
