<script setup>
import { reactive, watch } from 'vue';

/**
 * @file WorkerForm.vue
 * @description 근무자를 추가하거나 수정하는 폼 컴포넌트입니다.
 * @props {boolean} isEditMode - true일 경우 '수정' 모드, false일 경우 '추가' 모드로 동작합니다.
 * @props {object|null} workerData - '수정' 모드일 때 폼에 채워넣을 기존 근무자 데이터입니다.
 */

// --- PROPS ---
const props = defineProps({
  isEditMode: {
    type: Boolean,
    default: false,
  },
  workerData: {
    type: Object,
    default: null,
  },
});

// --- STATE ---

/**
 * @description 폼의 각 입력 필드와 연결될 반응형 데이터 객체입니다.
 */
const formData = reactive({
  image: null,
  employeeId: '',
  name: '',
  position: '',
  phone: '',
  startDate: null,
  endDate: null,
});

// --- WATCHERS ---

/**
 * @description props로 전달된 workerData가 변경될 때마다 formData를 업데이트합니다.
 * @description 이를 통해 '수정' 모드에서 폼에 초기 데이터를 채울 수 있습니다.
 */
watch(() => props.workerData, (newData) => {
  if (newData) {
    formData.employeeId = newData.employeeId || '';
    formData.name = newData.name || '';
    formData.position = newData.position || '';
    formData.phone = newData.phone || '';
    // startDate, endDate, image 등도 동일하게 처리
  } else {
    // workerData가 null이면 (예: 추가 모드 전환 시) 폼을 초기화합니다.
    Object.keys(formData).forEach(key => formData[key] = null);
    formData.employeeId = '';
    formData.name = '';
    formData.position = '';
    formData.phone = '';
  }
}, { immediate: true }); // 컴포넌트가 마운트될 때 즉시 실행

// --- METHODS ---

const handleSubmit = () => {
  if (props.isEditMode) {
    console.log('수정 데이터 전송:', formData);
    // 부모에게 'update-worker' 이벤트 emit
  } else {
    console.log('추가 데이터 전송:', formData);
    // 부모에게 'add-worker' 이벤트 emit
  }
};

const handleCancel = () => {
  console.log('폼 취소');
  // 부모에게 'cancel' 이벤트 emit
};
</script>

<template>
  <div class="form-wrapper">
    <form @submit.prevent="handleSubmit">
      <div class="form-group image-uploader">
        <div class="image-preview">
          </div>
        <div class="image-info">
          <p>Please upload square image, size less than 100KB</p>
          <button type="button" class="choose-file-btn">Choose File</button>
          <span>No File Chosen</span>
        </div>
      </div>
      
      <div class="fields-grid">
        <div class="form-group">
          <label for="employeeId">Employee ID Number *</label>
          <input type="text" id="employeeId" v-model="formData.employeeId" required />
        </div>
        <div class="form-group">
          <label for="workerName">Worker Name *</label>
          <input type="text" id="workerName" v-model="formData.name" required />
        </div>
        <div class="form-group">
          <label for="position">Position *</label>
          <input type="text" id="position" v-model="formData.position" required />
        </div>
        <div class="form-group">
          <label for="phoneNumber">Phone Number *</label>
          <input type="tel" id="phoneNumber" v-model="formData.phone" required />
        </div>
      </div>
      
      <div class="form-group">
        <label>Date Range *</label>
        <div class="date-picker-placeholder">
          달력 컴포넌트가 여기에 표시됩니다.
        </div>
      </div>
      
      <div class="form-actions">
        <button type="button" class="cancel-btn" @click="handleCancel">Cancel</button>
        <button type="submit" class="submit-btn">
          {{ isEditMode ? 'Edit' : 'Add' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.form-wrapper {
  padding: 2rem;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  height: 100%;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  /* 👇 박스 크기 계산 방식을 일관성 있게 하여 정렬 오류를 방지합니다. */
  box-sizing: border-box; 
}

.image-uploader {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.image-preview {
  width: 100px;
  height: 100px;
  background-color: #f0f0f0;
  border: 1px dashed #ccc;
  border-radius: 4px;
}
.image-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.image-info p {
  font-size: 0.8rem;
  color: #666;
  margin: 0;
}
.file-input-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}


/* 👇 [핵심 수정] 이 부분을 통해 정렬과 간격 문제를 동시에 해결합니다. */
.fields-grid {
  display: grid;                  /* Grid 레이아웃을 사용합니다. */
  grid-template-columns: 1fr 1fr; /* 1:1 비율의 동일한 컬럼 2개를 생성합니다. */
  column-gap: 1.5rem;             /* 컬럼과 컬럼 사이에 1.5rem의 간격을 만듭니다. */
}


.date-picker-placeholder {
  height: 200px;
  background-color: #f0f0f0;
  border: 1px dashed #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.form-actions button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
}

.cancel-btn {
  background-color: #f0f0f0;
  color: #333;
}

.submit-btn {
  background-color: #007bff;
  color: #fff;
}
</style>