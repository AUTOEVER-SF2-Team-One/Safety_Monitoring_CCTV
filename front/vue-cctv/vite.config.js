import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // 환경 변수 로드
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [
      vue(),
      vueDevTools(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      port: parseInt(env.VITE_SERVER_PORT) || 5173,
      host: env.VITE_SERVER_HOST || 'localhost',
      strictPort: true, // 포트가 사용 중이면 에러 발생
      open: true, // 개발 서버 시작 시 브라우저 자동 열기
      cors: true, // CORS 활성화
      proxy: {
        // API 프록시 설정 (CORS 우회)
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:8080',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
          secure: false,
        }
      }
    },
    preview: {
      port: parseInt(env.VITE_SERVER_PORT) || 5173,
      host: env.VITE_SERVER_HOST || 'localhost',
      strictPort: true,
    },
    define: {
      // 환경 변수를 클라이언트에서 사용할 수 있도록 정의
      __APP_VERSION__: JSON.stringify(env.npm_package_version || '1.0.0'),
    }
  }
})
