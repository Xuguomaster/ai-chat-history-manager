import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // 设置 @ 别名指向 src 目录
      '@': resolve(__dirname, 'src')
    }
  },
  server: {
    port: 3000,
    // 代理配置：将 /api 请求转发到后端服务
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
