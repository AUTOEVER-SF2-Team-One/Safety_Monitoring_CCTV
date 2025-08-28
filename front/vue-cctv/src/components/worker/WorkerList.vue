<script setup>
import { ref, computed } from 'vue';
import WorkerCard from '@/components/worker/WorkerCard.vue';

// --- PROPS ---
/**
 * @props {Array<object>} workers - 부모 컴포넌트로부터 전달받은 전체 근무자 목록
 */
const props = defineProps({
  workers: {
    type: Array,
    required: true,
  }
});

// --- EMITS ---
/**
 * @emits add-worker - 'Add Worker' 버튼 클릭 시 부모에게 알림
 * @emits select-worker - 특정 근무자 카드 선택 시 부모에게 알림 (선택된 근무자 객체 전달)
 * @emits delete-worker - 특정 근무자 삭제 시 부모에게 알림 (삭제할 근무자 ID 전달)
 */
const emit = defineEmits(['add-worker', 'select-worker', 'delete-worker']);

// --- STATE ---
const searchTerm = ref('');

// --- COMPUTED ---
const filteredWorkers = computed(() => {
  if (!searchTerm.value.trim()) {
    return props.workers;
  }
  return props.workers.filter(worker =>
    worker.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});

// --- METHODS ---
// 이제 모든 핸들러는 부모에게 이벤트를 emit하는 역할만 합니다.
const handleAddWorker = () => {
  emit('add-worker');
};

const handleSelectWorker = (worker) => {
  emit('select-worker', worker);
};

const handleDeleteWorker = (workerId) => {
  emit('delete-worker', workerId);
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
        <WorkerCard 
          :worker="worker" 
          @select-worker="handleSelectWorker(worker)"
          @delete-worker="handleDeleteWorker"
        />
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