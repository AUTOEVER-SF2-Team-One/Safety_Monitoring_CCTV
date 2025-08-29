import axios from 'axios';
import { getApiConfig } from '../config/config.js';

// API 설정 가져오기
const { baseURL, timeout } = getApiConfig();

console.log('API 설정:', { baseURL, timeout });

// 개발 환경에서는 프록시 경로 사용 (CORS 우회)
const isDevelopment = import.meta.env.DEV;
const apiBaseURL = isDevelopment ? '/api' : baseURL;

console.log('실제 API URL:', apiBaseURL);

// axios 기본 설정
const api = axios.create({
  baseURL: apiBaseURL,
  timeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터
api.interceptors.request.use(
  (config) => {
    console.log('API 요청:', config.method?.toUpperCase(), config.url);
    console.log('요청 데이터:', config.data);
    return config;
  },
  (error) => {
    console.error('요청 인터셉터 오류:', error);
    return Promise.reject(error);
  }
);

// 응답 인터셉터
api.interceptors.response.use(
  (response) => {
    console.log('API 응답:', response.status, response.config.url);
    console.log('응답 데이터:', response.data);
    return response;
  },
  (error) => {
    console.error('API 오류:', error.response?.status, error.response?.data);
    
    // 에러 응답이 있는 경우 상세 정보 로깅
    if (error.response) {
      const { status, data } = error.response;
      console.error(`HTTP ${status}:`, data);
    } else if (error.request) {
      console.error('네트워크 오류:', error.message);
    } else {
      console.error('요청 설정 오류:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default api;
