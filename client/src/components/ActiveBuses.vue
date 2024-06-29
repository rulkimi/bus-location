<template>
  <div class="flex flex-wrap">
    <div
      v-if="routes.length"
      v-for="route in routes"
      :key="route"
      class="bg-white shadow-md rounded-lg mb-2 px-4 py-2 cursor-pointer hover:bg-gray-100 mr-2"
      @click="fetchLocation(route)"
      style="max-width: calc(100% - 4px);"
    >
      {{ route }}
    </div>
    <div v-else>No route available now.</div>
  </div>
</template>

<script>
export default {
  emits: ['fetch-location'],
  props: {
    routes: {
      type: Array,
      required: true
    }
  },
  methods: {
    fetchLocation(route) {
      this.$emit('fetch-location', route);
    }
  }
}
</script>