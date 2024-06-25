import { createApp } from 'vue';
import App from './App.vue';
import "leaflet/dist/leaflet.css";
import './index.css'
import { Icon } from 'leaflet';

// Import the marker images using ES module syntax
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png';
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

// Fix for the missing marker icons issue
delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: iconRetina,
  iconUrl: iconUrl,
  shadowUrl: shadowUrl,
});

createApp(App).mount('#app');
