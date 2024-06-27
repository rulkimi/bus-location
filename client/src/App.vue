<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="container mx-auto px-4 py-8">
      <!-- Available Routes List -->
      <div class="mt-4">
        <h1 class="text-2xl font-bold mb-4">Available Routes:</h1>
        <active-buses :routes="routes" @fetch-location="fetchLocation" />
      </div>

      <div class="mt-4">
        <h1 class="text-2xl font-bold mb-4">Bus Location</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Left side (1/3 width on medium screens and larger) -->
          <div class="md:col-span-1">
            <div class="bg-white p-6 rounded-lg shadow-md">
              <input
                type="text"
                v-model="routeId"
                class="route-input border border-gray-300 px-3 py-2 rounded-md w-full mb-4"
                placeholder="Search route ID here or click from the list above"
              />
              <button
                @click="fetchLocation(routeId)"
                class="bg-blue-500 text-white px-4 py-2 rounded-md w-full"
                :class="loading ? 'opacity-75' : 'hover:bg-blue-600'"
                :disabled="loading"
              >
                  Search
              </button>
              <bus-list :buses="buses" @bus-selected="setMapView" class="mt-4" />
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
  </div>
</template>

<script>
import ActiveBuses from './components/ActiveBuses.vue';
import BusMap from './components/BusMap.vue';
import BusList from './components/BusList.vue';

export default {
  name: 'App',
  components: {
    BusMap,
    BusList,
    ActiveBuses
  },
  data() {
    return {
      routeId: '',
      buses: [],
      routes: [],
      loading: false
    };
  },
  async mounted() {
    await this.fetchAllRoutes();
  },
  methods: {
    async fetchLocation(routeId) {
      this.loading = true;
      this.routeId = routeId;
      try {
        const response = await fetch(`http://localhost:8000/vehicle/${routeId}`);
        const responseData = await response.json();
        this.buses = responseData.vehicles;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    async fetchAllRoutes() {
      try {
        const response = await fetch(`http://localhost:8000/routes`);
        const responseData = await response.json();
        this.routes = responseData.active_routes;
      } catch (error) {
        console.error(error);
      }
    },
    setMapView({ latitude, longitude, vehicleId }) {
      this.$refs.busMap.center = [latitude, longitude];
      this.$refs.busMap.zoom = 50;
      this.$refs.busMap.openMarkerPopup(latitude, longitude);
    },
    selectRoute(route) {
      this.routeId = route; // Set the selected route to the input field
    }
  }
};
</script>
