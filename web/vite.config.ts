import { defineConfig } from "vite";

export default defineConfig({
  base: "./",
  build: {
    sourcemap: true,
    chunkSizeWarningLimit: 1200, // kB; MapLibre GL alone is about 1000 kB minified.
  },
});
