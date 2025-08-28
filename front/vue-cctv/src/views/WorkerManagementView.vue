<script setup>
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

</script>

<template>
  <div class="worker-management-container">
    <section class="list-section">
      <WorkerList />
    </section>

    <section class="form-section">
      <WorkerForm />
    </section>
  </div>
</template>

<style scoped>
.worker-management-container {
  display: flex; /* 자식 요소들을 가로로 배치 (Flexbox) */
  gap: 2rem;   /* 두 섹션 사이의 간격 */
  padding: 1rem;
}

.list-section {
  /* flex-grow, flex-shrink, flex-basis를 한 번에 쓰는 속성입니다. */
  /* 여기서는 전체 공간의 40%를 차지하도록 설정합니다. */
  flex: 0 0 40%;
  max-width: 500px; /* 최대 너비 설정 */
}

.form-section {
  /* 나머지 공간을 모두 차지하도록 설정합니다. */
  flex: 1;
}
</style>