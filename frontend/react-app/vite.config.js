import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy API requests to the backend Flask server
      '/api': {
        target: 'http://127.0.0.1:5001',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
        // Ensure Authorization and other headers are forwarded to the backend
        configure: (proxy, options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            try {
              const auth = req.headers['authorization'] || req.headers['Authorization']
              if (auth) {
                proxyReq.setHeader('Authorization', auth)
              }
              // forward cookies if present
              if (req.headers.cookie) {
                proxyReq.setHeader('Cookie', req.headers.cookie)
              }
            } catch (e) {
              console.error('Error while configuring proxy headers for request:', req?.url, e)
            }
          })
        }
      }
    }
  }
})
