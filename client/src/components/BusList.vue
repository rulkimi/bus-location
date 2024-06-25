<template>
  <ul class="bus-list">
    <li v-for="bus in buses" :key="bus.info.vehicle_id">
      <div @click="handleClick(bus.info.latitude, bus.info.longitude, bus.info.vehicle_id)">
        {{ bus.info.vehicle_id }} - {{ bus.location }}
      </div>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'BusList',
  props: {
    buses: Array
  },
  methods: {
    handleClick(latitude, longitude, vehicleId) {
      this.$emit('busSelected', { latitude, longitude, vehicleId });
    }
  }
};
</script>

<style scoped>
.bus-list {
  list-style-type: none;
  padding: 0;
}
.bus-list li {
  cursor: pointer;
}
</style>
