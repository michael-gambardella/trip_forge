import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// BACKEND_HOST can be overridden via environment variable.
// Defaults to localhost for local dev; set to http://backend:8000 in Docker.
const backendHost = process.env.BACKEND_HOST ?? "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      "/api": {
        target: backendHost,
        changeOrigin: true,
      },
    },
  },
});
