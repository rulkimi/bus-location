<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Left side (1/3 width on medium screens and larger) -->
        <div class="md:col-span-1">
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h1 class="text-2xl font-bold mb-4">Bus Locations Map</h1>
            <input
              type="text"
              v-model="routeId"
              class="route-input border border-gray-300 px-3 py-2 rounded-md w-full mb-4"
              placeholder="Enter route ID"
            />
            <button
              @click="fetchLocation"
              class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md w-full"
            >
              Search
            </button>
            <bus-list :buses="buses" @busSelected="setMapView" class="mt-4" />
          </div>
        </div>
        <!-- Right side (2/3 width on medium screens and larger) -->
        <div class="md:col-span-2">
          <div class="bg-white p-6 rounded-lg shadow-md">
            <bus-map :buses="buses" ref="busMap" class="h-96" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BusMap from './components/BusMap.vue';
import BusList from './components/BusList.vue';

export default {
  name: 'App',
  components: {
    BusMap,
    BusList
  },
  data() {
    return {
      routeId: 'T8150',
      buses: []
    };
  },
  methods: {
    async fetchLocation() {
      try {
        const response = await fetch(`http://localhost:8000/vehicle/${this.routeId}`);
        const responseData = await response.json();
        this.buses = responseData.vehicles;
      } catch (error) {
        console.error(error);
      }
    },
    setMapView({ latitude, longitude, vehicleId }) {
      this.$refs.busMap.center = [latitude, longitude];
      this.$refs.busMap.zoom = 50;
      this.$refs.busMap.openMarkerPopup(latitude, longitude);
    },
  }
};
</script>
