/**
 * 애플리케이션 설정 파일
 * 개발/프로덕션 환경에 따른 설정 관리
 */

const config = {
  // 개발 환경 설정
  development: {
    api: {
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080',
      timeout: parseInt(import.meta.env.VITE_API_TIMEOUT) || 10000,
    },
    server: {
      port: parseInt(import.meta.env.VITE_SERVER_PORT) || 5173,
      host: import.meta.env.VITE_SERVER_HOST || 'localhost',
    },
    app: {
      title: import.meta.env.VITE_APP_TITLE || 'CCTV 안전 모니터링 시스템 (개발)',
      version: '1.0.0',
      debug: true,
    }
  },
  // 프로덕션 환경 설정
  production: {
    api: {
      baseURL: import.meta.env.VITE_API_BASE_URL || 'https://your-production-domain.com',
      timeout: parseInt(import.meta.env.VITE_API_TIMEOUT) || 15000,
    },
    server: {
      port: parseInt(import.meta.env.VITE_SERVER_PORT) || 80,
      host: import.meta.env.VITE_SERVER_HOST || '0.0.0.0',
    },
    app: {
      title: import.meta.env.VITE_APP_TITLE || 'CCTV 안전 모니터링 시스템',
      version: '1.0.0',
      debug: false,
    }
  },
};

// 현재 환경 감지
const currentEnv = import.meta.env.MODE || 'development';

// 환경별 설정 반환
export const getConfig = () => {
  return config[currentEnv] || config.development;
};

// API 설정만 반환
export const getApiConfig = () => {
  return getConfig().api;
};

// 서버 설정만 반환
export const getServerConfig = () => {
  return getConfig().server;
};

// 앱 설정만 반환
export const getAppConfig = () => {
  return getConfig().app;
};

// 현재 환경 정보 반환
export const getCurrentEnvironment = () => {
  return {
    mode: currentEnv,
    isDevelopment: currentEnv === 'development',
    isProduction: currentEnv === 'production',
  };
};

export default config;
