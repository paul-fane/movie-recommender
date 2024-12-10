import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
// export default defineConfig({
//   server: {
//     hmr: {
//       host: 'localhost', // Use Docker host's name or IP
//     },
//     //host: '0.0.0.0', // Listen on all interfaces
//     port: 5173,      // Optional: Specify the port
//     strictPort: true // Prevent fallback to another port
//   },
//   plugins: [react()],
// })

// export default defineConfig({
//   base: "/",
//   plugins: [react()],
//   preview: {
//    port: 8080,
//    strictPort: true,
//   },
//   server: {
//    port: 8080,
//    strictPort: true,
//    host: true,
//    origin: "http://0.0.0.0:8080",
//   },
//  });


 export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    watch: {
       usePolling: true,
    },
  },
});
