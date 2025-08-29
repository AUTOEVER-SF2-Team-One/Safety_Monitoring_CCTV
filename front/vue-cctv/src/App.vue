<script setup>
import { RouterView } from 'vue-router'
import { getAppConfig, getCurrentEnvironment, getServerConfig } from './config/config.js'

// 설정 정보 가져오기
const appConfig = getAppConfig()
const serverConfig = getServerConfig()
const envInfo = getCurrentEnvironment()
</script>

<template>
  <div id="app">
    <!-- 네비게이션 바 -->
    <nav class="navbar">
      <div class="nav-container">
        <h1 class="nav-title">{{ appConfig.title }}</h1>
        <div class="nav-links">
          <router-link to="/worker" class="nav-link">작업자 관리</router-link>
          <router-link to="/api-test" class="nav-link">API 테스트</router-link>
        </div>
      </div>
    </nav>

    <!-- 환경 정보 표시 (개발 환경에서만) -->
    <div v-if="envInfo.isDevelopment" class="env-info">
      <div class="env-container">
        <span class="env-badge development">개발 환경</span>
        <span class="env-detail">프론트엔드: localhost:{{ serverConfig.port }}</span>
        <span class="env-detail">백엔드: localhost:8080</span>
        <span class="env-version">v{{ appConfig.version }}</span>
      </div>
    </div>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
/* 기본적인 스타일을 여기에 추가할 수 있습니다. */
main {
  padding: 2rem;
}

/* 네비게이션 바 스타일 */
.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
}

.nav-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: #34495e;
}

.nav-link.router-link-active {
  background-color: #3498db;
}

/* 환경 정보 스타일 */
.env-info {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
  padding: 0.5rem 0;
}

.env-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6c757d;
}

.env-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
}

.env-badge.development {
  background-color: #17a2b8;
  color: white;
}

.env-detail {
  color: #495057;
}

.env-version {
  margin-left: auto;
  color: #6c757d;
  font-style: italic;
}
</style>