import os
from dotenv import load_dotenv
import telebot
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from requests import get
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
USER_AGENT = os.getenv('EMAIL')

print(USER_AGENT)
print(BOT_TOKEN)

bot = telebot.TeleBot(BOT_TOKEN)

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

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['routes'])
def send_routes(message):
    bot.reply_to(message, "Fetching active routes data. Wait a moment...")

    feed_content = fetch_gtfs_realtime_feed(URL)
    if not feed_content:
        bot.reply_to(message, "Failed to fetch bus data.")
        return

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(feed_content)
    vehicles = [MessageToDict(entity.vehicle) for entity in feed.entity]

    active_routes = set(vehicle.get('trip', {}).get('routeId', 'N/A') for vehicle in vehicles)

    routes_list = '\n'.join(f"{i+1}. {route}" for i, route in enumerate(active_routes))
    bot.reply_to(message, f"Active Bus Routes:\n{routes_list}")

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    bot.reply_to(message, "Searching for information...")

    bus_route = message.text.strip().lower()

    feed_content = fetch_gtfs_realtime_feed(URL)
    if not feed_content:
        bot.reply_to(message, "Failed to fetch bus data.")
        return

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(feed_content)
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

    for vehicle in structured_vehicles:
        if bus_route == vehicle.route_id.lower():
            location_name = reverse_geocode(vehicle.latitude, vehicle.longitude)
            bot.send_message(message.chat.id, f'Bus found:\n{vehicle}\nLocation: {location_name}')
            bot.send_location(message.chat.id, vehicle.latitude, vehicle.longitude)
            break
    else:
        bot.reply_to(message, 'No bus found for the specified route.')

bot.infinity_polling()
