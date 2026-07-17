import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

<<<<<<< HEAD
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
=======
// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
>>>>>>> 716eefe (Add React frontend structure)
})
