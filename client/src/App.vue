<template>
  <div>
    <h1>Bus Locations Map</h1>
    <input type="text" v-model="routeId" class="route-input" placeholder="Enter route ID">
    <button @click="fetchLocation">Search</button>
    <bus-list :buses="buses" @busSelected="setMapView" />
    <bus-map :buses="buses" ref="busMap" />
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
      routeId: 't8150',
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

<style>
/* Add any global styles here */
</style>
