import { MapLibreMap } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import "./style.css";

const container = document.getElementById("map");
if (container === null) {
  throw new Error("Missing #map element");
}

new MapLibreMap({
  container,
  style: {
    version: 8,
    sources: {},
    layers: [{ id: "background", type: "background", paint: { "background-color": "#dde3e8" } }],
  },
  center: [30, 25],
  zoom: 2,
});
