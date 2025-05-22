import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Django DRF 서버 주소
        changeOrigin: true,
        secure: false,                   // HTTPS 아닌 경우 false 설정
        rewrite: path => path.replace(/^\/api/, '/api'),  // 생략 가능하지만 명시해둬도 OK
      },
    },
  },
})
