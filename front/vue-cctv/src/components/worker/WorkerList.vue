<script setup>
import { ref, computed } from 'vue';
import WorkerCard from '@/components/worker/WorkerCard.vue';

/**
 * @file WorkerList.vue
 * @description 근무자 목록을 표시하고 관리하는 컴포넌트입니다.
 * @description 검색, 추가, 목록 렌더링 기능을 담당합니다.
 */

// --- STATE ---

/**
 * @type {import('vue').Ref<Array<object>>}
 * @description API로부터 받아온 근무자 목록을 저장하는 반응형 상태입니다.
 * @property {number} id - 근무자 고유 ID
 * @property {string} name - 근무자 이름
 * @property {string} position - 직책
 * @property {string} period - 근무 기간
 * @property {string} phone - 연락처
 */
const workers = ref([
  { id: 1, name: 'Sarah Johnson', position: 'Safety Inspector', period: '2025.08.22-2025.09.05', phone: '+1(555) 987-6543' },
  { id: 2, name: 'Daniel Kim', position: 'Safety Inspector', period: '2025.08.22-2025.09.05', phone: '+1(555) 987-6543' },
  { id: 3, name: 'Bake Cook', position: 'Safety Inspector', period: '2025.08.22-2025.09.05', phone: '+1(555) 987-6543' }
]);

/**
 * @type {import('vue').Ref<string>}
 * @description 사용자가 입력한 검색어를 저장하는 반응형 상태입니다.
 */
const searchTerm = ref('');

// --- COMPUTED ---

/**
 * @type {import('vue').ComputedRef<Array<object>>}
 * @description `searchTerm`을 기반으로 `workers` 배열을 필터링한 결과를 반환하는 계산된 속성입니다.
 * @description 검색어가 없으면 전체 목록을, 있으면 이름에 검색어가 포함된 목록을 반환합니다.
 */
const filteredWorkers = computed(() => {
  if (!searchTerm.value.trim()) {
    return workers.value;
  }
  return workers.value.filter(worker =>
    worker.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});

// --- METHODS ---

/**
 * @description 'Add Worker' 버튼 클릭 시 호출되는 이벤트 핸들러입니다.
 * @description 현재는 콘솔에 로그만 출력하며, 향후 부모 컴포넌트로 이벤트를 발생시켜
 * @description 근무자 추가 폼을 활성화하는 역할을 합니다.
 */
const handleAddWorker = () => {
  console.log('handleAddWorker called: 부모 컴포넌트에 "add-worker" 이벤트 emit 예정');
  // emit('add-worker');
};
</script>

<template>
  <div class="worker-list-wrapper">
    <header class="list-header">
      <h1>Worker List</h1>
      <div class="search-bar">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
          <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
        </svg>
        <input type="text" v-model="searchTerm" placeholder="Search Worker..." />
      </div>
    </header>

    <ul class="worker-cards">
      <li v-for="worker in filteredWorkers" :key="worker.id">
        <WorkerCard :worker="worker" />
      </li>
    </ul>
    
    <footer class="list-footer">
      <button class="add-button" @click="handleAddWorker">Add Worker</button>
    </footer>
  </div>
</template>

<style scoped>
/* 이전과 동일 */
.worker-list-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.list-header h1 {
  font-size: 1.75rem;
  font-weight: bold;
  margin-bottom: 1rem;
}
.search-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  margin-bottom: 1.5rem;
}
.search-bar svg {
  color: #888;
}
.search-bar input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 1rem;
}
.worker-cards {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
  flex: 1;
}
.worker-cards li {
  margin-bottom: 1rem;
}
.list-footer {
  margin-top: 1.5rem;
}
.add-button {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.add-button:hover {
  background-color: #0056b3;
}
</style>