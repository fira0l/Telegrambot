import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Flask API endpoints
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      },
      // Flask form submit and other routes
      '/submit-order': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      },
      // Serve Flask static assets if needed
      '/static': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
