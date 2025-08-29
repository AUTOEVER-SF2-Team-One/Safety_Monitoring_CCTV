<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <!-- 네비게이션 바 -->
    <nav class="navbar">
      <div class="nav-container">
        <h1 class="nav-title">CCTV 안전 모니터링 시스템</h1>
        <div class="nav-links">
          <router-link to="/worker" class="nav-link">작업자 관리</router-link>
          <router-link to="/api-test" class="nav-link">API 테스트</router-link>
        </div>
      </div>
    </nav>

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
</style>