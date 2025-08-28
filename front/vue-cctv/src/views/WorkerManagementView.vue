<script setup>
import { ref, computed } from 'vue';
import WorkerList from '@/components/worker/WorkerList.vue';
import WorkerForm from '@/components/worker/WorkerForm.vue';

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
 * @description WorkerList에 표시될 전체 근무자 목록입니다. (가짜 데이터)
 */
 const workers = ref([
 { id: 1, employeeId: '201902927', name: 'Sarah Johnson', position: 'Safety Inspector', phone: '+1(555) 987-6543', workingDates: ['2025-08-22', '2025-08-23', '2025-08-25'], image: null },
  { id: 2, employeeId: '202011234', name: 'Daniel Kim', position: 'Safety Inspector', phone: '+1(555) 987-6543', workingDates: ['2025-09-01', '2025-09-02'], image: null },
  { id: 3, employeeId: '202105678', name: 'Bake Cook', position: 'Safety Inspector', phone: '+1(555) 987-6543', workingDates: ['2025-08-28'], image: null }
]);

// --- COMPUTED ---

/**
 * @description 폼이 '수정' 모드인지 여부를 계산합니다.
 * @returns {boolean}
 */
 const isEditMode = computed(() => formMode.value === 'edit');


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
 * @description 신규 근무자 데이터를 workers 배열에 추가합니다. (WorkerForm으로부터 이벤트 수신)
 * @param {object} newWorker - WorkerForm에서 전달된 신규 근무자 데이터
 */
 const addWorker = (newWorker) => {
  // 실제 애플리케이션에서는 백엔드 API로부터 ID를 받아야 합니다.
  // 여기서는 임시로 고유한 ID를 생성합니다.
  const workerWithId = { ...newWorker, id: Date.now() };
  workers.value.push(workerWithId);
  console.log('Added new worker:', workerWithId);
  closeForm(); // 추가 후 폼 닫기
};

/**
 * @description 기존 근무자 데이터를 수정합니다. (WorkerForm으로부터 이벤트 수신)
 * @param {object} updatedWorker - WorkerForm에서 전달된 수정된 근무자 데이터
 */
 const updateWorker = (updatedWorker) => {
  const index = workers.value.findIndex(w => w.id === updatedWorker.id);
  if (index !== -1) {
    workers.value[index] = updatedWorker;
    console.log('Updated worker:', updatedWorker);
  }
  closeForm(); // 수정 후 폼 닫기
};

/**
 * @description 근무자 삭제 시 호출됩니다. (WorkerList로부터 이벤트 수신)
 * @param {number} workerId - 삭제할 근무자 ID
 */
 const deleteWorker = (workerId) => {
  if (confirm('정말로 이 근무자를 삭제하시겠습니까?')) {
    workers.value = workers.value.filter(w => w.id !== workerId);
    console.log(`Worker with id ${workerId} deleted.`);
    // 폼이 열려있고, 삭제된 근무자가 선택된 근무자였다면 폼을 닫습니다.
    if (selectedWorker.value && selectedWorker.value.id === workerId) {
      closeForm();
    }
  }
};
</script>

<template>
  <div class="worker-management-container">
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
</style>
