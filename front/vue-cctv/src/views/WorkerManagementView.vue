<script setup>
import { ref, computed, onMounted } from 'vue';
import WorkerList from '@/components/worker/WorkerList.vue';
import WorkerForm from '@/components/worker/WorkerForm.vue';
import { workerService } from '@/services/workerService.js';

// --- STATE ---

/**
 * @description 폼의 현재 상태를 관리합니다.
 * 'add': 추가 모드, 'edit': 수정 모드, null: 닫힘 상태
 * @type {import('vue').Ref<'add' | 'edit' | null>}
 */
 const formMode = ref(null); // 초기에는 폼이 닫혀있음

 /**
 * @description 수정할 근무자의 데이터를 저장합니다.
 * @type {import('vue').Ref<object | null>}
 */
const selectedWorker = ref(null);

/**
 * @description WorkerList에 표시될 전체 근무자 목록입니다.
 */
const workers = ref([]);

/**
 * @description 로딩 상태를 관리합니다.
 */
const isLoading = ref(false);

/**
 * @description 에러 메시지를 관리합니다.
 */
const errorMessage = ref('');

// --- COMPUTED ---

/**
 * @description 폼이 '수정' 모드인지 여부를 계산합니다.
 * @returns {boolean}
 */
const isEditMode = computed(() => formMode.value === 'edit');

// --- LIFECYCLE ---

/**
 * @description 컴포넌트 마운트 시 작업자 목록을 로드합니다.
 */
onMounted(async () => {
  await loadWorkers();
});

// --- METHODS (API Calls) ---

/**
 * @description 백엔드에서 작업자 목록을 로드합니다.
 */
const loadWorkers = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';
    const data = await workerService.getAllWorkers();
    workers.value = data;
  } catch (error) {
    errorMessage.value = '작업자 목록을 불러오는데 실패했습니다.';
    console.error('작업자 목록 로드 실패:', error);
  } finally {
    isLoading.value = false;
  }
};


// --- METHODS (Event Handlers) ---

/**
 * @description 'Add Worker' 버튼 클릭 시 호출됩니다. (WorkerList로부터 이벤트 수신)
 */
const openAddForm = () => {
  formMode.value = 'add';
  selectedWorker.value = null; // 수정 모드에서 사용된 데이터를 초기화
};

/**
 * @description 근무자 카드 클릭 시 호출됩니다. (WorkerList로부터 이벤트 수신)
 * @param {object} worker - 선택된 근무자 객체
 */
const openEditForm = (worker) => {
  formMode.value = 'edit';
  selectedWorker.value = worker;
};

/**
 * @description 폼에서 'Cancel' 버튼 클릭 시 호출됩니다. (WorkerForm으로부터 이벤트 수신)
 */
const closeForm = () => {
  formMode.value = null;
  selectedWorker.value = null;
};

/**
 * @description 신규 근무자 데이터를 백엔드에 추가합니다. (WorkerForm으로부터 이벤트 수신)
 * @param {object} newWorker - WorkerForm에서 전달된 신규 근무자 데이터
 */
const addWorker = async (newWorker) => {
  try {
    isLoading.value = true;
    errorMessage.value = '';
    const createdWorker = await workerService.createWorker(newWorker);
    workers.value.push(createdWorker);
    console.log('Added new worker:', createdWorker);
    closeForm(); // 추가 후 폼 닫기
  } catch (error) {
    errorMessage.value = '작업자 추가에 실패했습니다.';
    console.error('작업자 추가 실패:', error);
  } finally {
    isLoading.value = false;
  }
};

/**
 * @description 기존 근무자 데이터를 백엔드에서 수정합니다. (WorkerForm으로부터 이벤트 수신)
 * @param {object} updatedWorker - WorkerForm에서 전달된 수정된 근무자 데이터
 */
const updateWorker = async (updatedWorker) => {
  try {
    isLoading.value = true;
    errorMessage.value = '';
    const result = await workerService.updateWorker(updatedWorker.id, updatedWorker);
    const index = workers.value.findIndex(w => w.id === updatedWorker.id);
    if (index !== -1) {
      workers.value[index] = result;
      console.log('Updated worker:', result);
    }
    closeForm(); // 수정 후 폼 닫기
  } catch (error) {
    errorMessage.value = '작업자 수정에 실패했습니다.';
    console.error('작업자 수정 실패:', error);
  } finally {
    isLoading.value = false;
  }
};

/**
 * @description 근무자를 백엔드에서 삭제합니다. (WorkerList로부터 이벤트 수신)
 * @param {number} workerId - 삭제할 근무자 ID
 */
const deleteWorker = async (workerId) => {
  if (confirm('정말로 이 근무자를 삭제하시겠습니까?')) {
    try {
      isLoading.value = true;
      errorMessage.value = '';
      await workerService.deleteWorker(workerId);
      workers.value = workers.value.filter(w => w.id !== workerId);
      console.log(`Worker with id ${workerId} deleted.`);
      // 폼이 열려있고, 삭제된 근무자가 선택된 근무자였다면 폼을 닫습니다.
      if (selectedWorker.value && selectedWorker.value.id === workerId) {
        closeForm();
      }
    } catch (error) {
      errorMessage.value = '작업자 삭제에 실패했습니다.';
      console.error('작업자 삭제 실패:', error);
    } finally {
      isLoading.value = false;
    }
  }
};
</script>

<template>
  <div class="worker-management-container">
    <!-- 에러 메시지 표시 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
      <button @click="errorMessage = ''" class="error-close-btn">×</button>
    </div>

    <!-- 로딩 오버레이 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>처리 중...</p>
    </div>

    <section class="list-section">
      <WorkerList
        :workers="workers"
        @add-worker="openAddForm"
        @select-worker="openEditForm"
        @delete-worker="deleteWorker"
      />
    </section>

    <section class="form-section">
      <WorkerForm
        v-if="formMode"
        :is-edit-mode="isEditMode"
        :worker-data="selectedWorker"
        @cancel="closeForm"
        @add-worker="addWorker"
        @update-worker="updateWorker"
      />
      <div v-else class="form-placeholder">
        <p>근무자를 추가하거나 목록에서 선택해주세요.</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.worker-management-container {
  display: flex;
  gap: 2rem;
  padding: 1rem;
  height: calc(100vh - 2rem); /* 화면 높이를 채우도록 설정 */
}

.list-section {
  flex: 0 0 40%;
  max-width: 500px;
}

.form-section {
  flex: 1;
}

.form-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  border: 2px dashed #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  color: #888;
}

/* 에러 메시지 스타일 */
.error-message {
  position: fixed;
  top: 20px;
  right: 20px;
  background-color: #f44336;
  color: white;
  padding: 12px 20px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 400px;
}

.error-close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 0;
  margin-left: auto;
}

.error-close-btn:hover {
  opacity: 0.8;
}

/* 로딩 오버레이 스타일 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 999;
  color: white;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
