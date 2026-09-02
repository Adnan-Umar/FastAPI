import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite config — dev server on port 5173 (matches the FastAPI CORS allow-list)
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
  },
})
