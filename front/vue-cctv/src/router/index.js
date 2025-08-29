import { createRouter, createWebHistory } from 'vue-router'
import WorkerManagementView from '@/views/WorkerManagementView.vue'
import ApiTestView from '@/views/ApiTestView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/worker', // 브라우저에 표시될 URL 경로
      name: 'worker-management',
      component: WorkerManagementView // 이 경로로 접속 시 보여줄 컴포넌트
    },
    {
      path: '/api-test', // API 테스트 페이지
      name: 'api-test',
      component: ApiTestView
    }
  ],
})

export default router
