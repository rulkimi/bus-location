// Initialize the map
const map = L.map('map').setView([2.922682, 101.64256], 50);

// Add a tile layer to the map (OpenStreetMap tiles)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Add a pin at the specified latitude and longitude
const initialMarker = L.marker([2.922682, 101.64256]).addTo(map);
initialMarker.bindPopup('<b>Initial Location</b>').openPopup();

// fetchLocation();

const busList = document.querySelector('.bus-list');
const markers = {};

async function fetchLocation() {
  const routeId = document.querySelector('.route-input').value;
  
  try {
    const response = await fetch(`http://localhost:8000/vehicle/${routeId}`);
    const responseData = await response.json();

    busList.innerHTML = '';

    const vehicles = responseData.vehicles;

    vehicles.forEach(vehicle => {
      const marker = L.marker([vehicle.info.latitude, vehicle.info.longitude]).addTo(map);
      const popupMessage = `
        <b>Vehicle ID:</b> ${vehicle.info.vehicle_id}<br>
        <b>Route ID:</b> ${vehicle.info.route_id}<br>
        <b>Timestamp:</b> ${vehicle.info.timestamp}<br>
        <b>Location:</b> ${vehicle.location}
      `;
      marker.bindPopup(popupMessage);
      markers[vehicle.info.vehicle_id] = marker;

      const busData = document.createElement("li");

      busData.innerHTML = `
        <div
          onClick="setMapView(${vehicle.info.latitude}, ${vehicle.info.longitude}, '${vehicle.info.vehicle_id}')"
        >
          ${vehicle.info.vehicle_id} - ${vehicle.location}
        </div>
      `;
      busList.appendChild(busData);
    });

    console.log(vehicles)

    setMapView(vehicles[0].info.latitude, vehicles[0].info.longitude, vehicles[0].info.vehicle_id);
  } catch (error) {
    console.error(error);
  }
}

function setMapView(latitude, longitude, vehicleId, zoom = 50) {
  map.setView([latitude, longitude], zoom);
  markers[vehicleId].openPopup();
}