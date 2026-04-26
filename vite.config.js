import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/analyze-profile': 'http://localhost:8000',
      '/risk-score': 'http://localhost:8000',
      '/match-opportunities': 'http://localhost:8000',
      '/country-pack': 'http://localhost:8000'
    }
  }
})
