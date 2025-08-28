<script setup>
/**
 * @file WorkerCard.vue
 * @description 개별 근무자의 정보를 표시하는 카드 컴포넌트입니다.
 * @description 부모로부터 근무자 객체를 props로 전달받습니다.
 * @description 카드 선택 또는 삭제 시 부모 컴포넌트로 이벤트를 전달합니다.
 */

// --- PROPS ---

/**
 * @props {Object} worker - 표시할 근무자 정보 객체.
 * @property {number} id - 근무자 고유 ID
 * @property {string} name - 근무자 이름
 * @property {string} position - 직책
 * @property {string} period - 근무 기간
 * @property {string} phone - 연락처
 */
const props = defineProps({
  worker: {
    type: Object,
    required: true,
  },
});

// --- EMITS ---

/**
 * @emits select-worker - 사용자가 카드를 클릭했을 때 발생하는 이벤트입니다.
 * @emits delete-worker - 사용자가 삭제 버튼을 클릭했을 때 발생하는 이벤트입니다. 근무자 id를 전달합니다.
 */
const emit = defineEmits(['select-worker', 'delete-worker']);

// --- METHODS ---

/**
 * @description 삭제 버튼 클릭 시 호출됩니다.
 * @description 부모에게 'delete-worker' 이벤트를 발생시키고 근무자 id를 전달합니다.
 */
const handleDelete = () => {
  emit('delete-worker', props.worker.id);
};

/**
 * @description 카드 자체를 클릭했을 때 호출됩니다.
 * @description 부모에게 'select-worker' 이벤트를 발생시킵니다. (ID 대신 객체 전체를 전달하도록 상위 컴포넌트에서 처리)
 */
 const handleSelect = () => {
  emit('select-worker'); // 인자 없이 이벤트만 발생
}
</script>

<template>
  <article class="worker-card" @click="handleSelect">
    <div class="card-info">
      <h3 class="worker-name">{{ worker.name }}</h3>
      <p class="worker-position">{{ worker.position }}</p>
      <div class="worker-details">
        <span class="detail-item">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
            <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5M1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4z"/>
          </svg>
          {{ worker.period }}
        </span>
        <span class="detail-item">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
            <path d="M3.654 1.328a.678.678 0 0 0-1.015-.063L1.605 2.3c-.483.484-.661 1.169-.45 1.77a17.6 17.6 0 0 0 4.168 6.608 17.6 17.6 0 0 0 6.608 4.168c.601.211 1.286.033 1.77-.45l1.034-1.034a.678.678 0 0 0-.063-1.015l-2.307-1.794a.68.68 0 0 0-.58-.122l-2.19.547a1.75 1.75 0 0 1-1.657-.459L5.482 8.062a1.75 1.75 0 0 1-.46-1.657l.548-2.19a.68.68 0 0 0-.122-.58zM1.884.511a1.745 1.745 0 0 1 2.612.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.68.68 0 0 0 .178.643l2.457 2.457a.68.68 0 0 0 .644.178l2.189-.547a1.75 1.75 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.6 18.6 0 0 1-7.01-4.42 18.6 18.6 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877z"/>
          </svg>
          {{ worker.phone }}
        </span>
      </div>
    </div>
    <div class="card-actions">
      <button class="delete-button" @click.stop="handleDelete">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
          <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
          <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
        </svg>
      </button>
    </div>
  </article>
</template>

<style scoped>
.worker-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out;
}

.worker-card:hover {
  border-color: #007bff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
}

.card-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.worker-name {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.worker-position {
  font-size: 0.9rem;
  color: #666;
  margin: 0;
}

.worker-details {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  margin-top: 0.75rem;
  font-size: 0.9rem;
  color: #333;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-item svg {
  color: #888;
}

.card-actions .delete-button {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: color 0.2s, background-color 0.2s;
}

.card-actions .delete-button:hover {
  color: #dc3545;
  background-color: #f8f9fa;
}
</style>