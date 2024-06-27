<template>
  <ul class="bus-list">
    <li v-for="bus in buses" :key="bus.info.vehicle_id" @click="handleClick(bus.info.latitude, bus.info.longitude, bus.info.vehicle_id)"
        class="bg-white shadow-md rounded-lg mb-2 px-4 py-2 cursor-pointer hover:bg-gray-100">
      <div>
        {{ bus.info.vehicle_id }} - {{ bus.location }}
      </div>
    </li>
  </ul>
</template>

<script>
export default {
  emits: ['bus-selected'],
  name: 'BusList',
  props: {
    buses: Array
  },
  methods: {
    handleClick(latitude, longitude, vehicleId) {
      this.$emit('bus-selected', { latitude, longitude, vehicleId });
    }
  }
};
</script>

<style scoped>
/* No need for additional styles if using Tailwind for all styling */
</style>
