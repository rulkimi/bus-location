<template>
  <l-map :zoom="zoom" :center="center" style="height: 600px; width: 100%;">
    <l-tile-layer :url="url" :attribution="attribution" />
    <l-marker
      v-for="bus in buses"
      :key="bus.info.vehicle_id"
      :lat-lng="[bus.info.latitude, bus.info.longitude]"
      ref="markers"
    >
      <l-popup>
        <div>
          <b>Vehicle ID:</b> {{ bus.info.vehicle_id }}<br>
          <b>Route ID:</b> {{ bus.info.route_id }}<br>
          <b>Timestamp:</b> {{ bus.info.timestamp }}<br>
          <b>Location:</b> {{ bus.location }}
        </div>
      </l-popup>
    </l-marker>
  </l-map>
</template>

<script>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet';

export default {
  name: 'BusMap',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup
  },
  props: {
    buses: Array
  },
  watch: {
    buses(newValue) {
      const firstBus = newValue[0];
      this.center = [firstBus.info.latitude, firstBus.info.longitude];

      this.$nextTick(() => {
        const markers = this.$refs.markers;
        if (markers) {
          const markerInstance = markers.find(marker =>
            marker.$props.latLng[0] === firstBus.info.latitude &&
            marker.$props.latLng[1] === firstBus.info.longitude
          );

          if (markerInstance && markerInstance.leafletObject) {
            // open the popup associated with the marker using leafletObject
            markerInstance.leafletObject.openPopup();
          } else {
            console.error('Marker instance or leafletObject not found:', markerInstance);
          }
        }
      });
    }
  },
  data() {
    return {
      center: [2.922682, 101.64256],
      zoom: 50,
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    };
  },
};
</script>

