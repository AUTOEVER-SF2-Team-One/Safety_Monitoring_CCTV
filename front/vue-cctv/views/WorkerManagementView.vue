<script setup>
import WorkerList from '@/components/worker/WorkerList.vue';
import WorkerForm from '@/components/worker/WorkerForm.vue';
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