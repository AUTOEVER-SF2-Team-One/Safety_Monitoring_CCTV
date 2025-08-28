<script setup>
import { ref,reactive, watch } from 'vue';
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

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

// --- EMITS ---

/**
 * @emits cancel - 사용자가 'Cancel' 버튼을 클릭했을 때 발생하는 이벤트입니다.
 * @emits add-worker - '추가' 모드에서 폼 제출 시, 신규 근무자 데이터를 담아 발생하는 이벤트입니다.
 * @emits update-worker - '수정' 모드에서 폼 제출 시, 수정된 근무자 데이터를 담아 발생하는 이벤트입니다.
 */
 const emit = defineEmits(['cancel', 'add-worker', 'update-worker']);

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
  workingDates: [],
});

/**
 * @description Datepicker와 v-model로 연결되어 선택된 모든 날짜를 배열로 가집니다.
 * @type {import('vue').Ref<Date[]>}
 */
 const selectedDates = ref([]);

 /**
 * @description 사용자가 선택한 이미지 파일 객체를 저장하는 ref입니다.
 * @type {import('vue').Ref<File|null>}
 */
const imageFile = ref(null);

/**
 * @description 선택된 이미지의 미리보기용 임시 URL을 저장하는 ref입니다.
 * @type {import('vue').Ref<string|null>}
 */
const imageUrl = ref(null);

/**
 * @description 파일 입력을 위한 <input type="file"> DOM 엘리먼트의 참조(reference)입니다.
 * @type {import('vue').Ref<HTMLInputElement|null>}
 */
 const fileInput = ref(null);

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
    selectedDates.value = (newData.workingDates || []).map(date => new Date(date));
    imageUrl.value = newData.image || null;
  } else {
    // workerData가 null이면 (예: 추가 모드 전환 시) 폼을 초기화합니다.
    Object.keys(formData).forEach(key => formData[key] = null);
    formData.employeeId = '';
    formData.name = '';
    formData.position = '';
    formData.phone = '';
    selectedDates.value = [];
    imageUrl.value = null;
    imageFile.value = null;
  }
}, { immediate: true }); // 컴포넌트가 마운트될 때 즉시 실행

/**
 * @description 사용자가 날짜를 선택/해제할 때마다 그 값을 formData에 즉시 반영합니다.
 */
 watch(selectedDates, (newDates) => {
  formData.workingDates = newDates || [];
}, { deep: true }); // 배열 내부의 변경을 감지하기 위해 deep 옵션 사용

// --- METHODS ---

/**
 * @function triggerFileInput
 * @description '사진 변경' 버튼 클릭 시, 숨겨진 파일 input 엘리먼트를 프로그래매틱하게 클릭하여 파일 선택창을 엽니다.
 */
 const triggerFileInput = () => {
  fileInput.value.click();
};

/**
 * @function handleImageUpload
 * @description 파일 input의 변경 이벤트를 처리합니다. 사용자가 파일을 선택하면 해당 파일을 상태에 저장하고,
 * 미리보기를 위한 임시 URL을 생성합니다.
 * @param {Event} event - 파일 input에서 발생한 change 이벤트 객체.
 */
const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file; // 파일 객체 저장

    // 기존에 생성된 Object URL이 있다면 메모리 누수 방지를 위해 해제합니다.
    if (imageUrl.value) {
      URL.revokeObjectURL(imageUrl.value);
    }
    // 선택된 파일로부터 새로운 Object URL을 생성하여 미리보기에 사용합니다.
    imageUrl.value = URL.createObjectURL(file);
  }
};

/**
 * @description 폼 제출(`submit`) 시 호출되는 이벤트 핸들러입니다.
 * @description `isEditMode` 값에 따라 'update-worker' 또는 'add-worker' 이벤트를 발생시킵니다.
 */
 const handleSubmit = () => {
  if (props.isEditMode) {
    const dataToEmit = { ...formData, image: imageUrl.value };
    // 수정 모드: 기존 id를 포함한 formData를 부모에게 전달
    emit('update-worker', { ...dataToEmit, id: props.workerData.id });
  } else {
    // 추가 모드: 새로운 formData를 부모에게 전달
    emit('add-worker', { ...dataToEmit });
  }
};

/**
 * @description 'Cancel' 버튼 클릭 시 호출되는 이벤트 핸들러입니다.
 * @description 부모에게 'cancel' 이벤트를 발생시켜 폼을 닫도록 요청합니다.
 */
const handleCancel = () => {
  emit('cancel');
};
</script>

<template>
  <div class="form-wrapper">
    <form @submit.prevent="handleSubmit">
      <div class="form-group image-uploader">
        <div class="image-preview">
            <img v-if="imageUrl" :src="imageUrl" alt="Image preview" />
        </div>
        <div class="image-info">
          <p>Please upload square image, size less than 100KB</p>

          <input 
            type="file" 
            ref="fileInput" 
            @change="handleImageUpload" 
            style="display: none" 
            accept="image/*"
          />
          
          <button 
            type="button" 
            class="choose-file-btn" 
            @click="triggerFileInput"
          >
            Choose File
          </button>
          
          <span>{{ imageFile ? imageFile.name : 'No File Chosen' }}</span>
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
        <label for="workingDates">Working Dates *</label>
        <Datepicker
          v-model="selectedDates"
          multi-dates
          :enable-time-picker="false"
          inline
          auto-apply
          class="inline-calendar"
        />
      </div>
      
      <div class="form-actions">
        <button type="button" class="cancel-btn" @click="$emit('cancel')">Cancel</button>
        <button type="submit" class="submit-btn">{{ isEditMode ? '수정' : '추가' }}</button>
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
  box-sizing: border-box; 
}

.image-uploader {
  display: flex;
  gap: 1rem;
  align-items: center;
}

/* --- ▼▼▼ 이미지 관련 보강된 스타일 ▼▼▼ --- */
.image-preview {
  width: 100px;
  height: 100px;
  background-color: #f0f0f0;
  border: 1px dashed #ccc;
  border-radius: 4px;
  /* 이미지가 중앙에 위치하도록 flex 속성 추가 */
  display: flex;
  justify-content: center;
  align-items: center;
  /* 이미지가 영역을 벗어나지 않도록 overflow: hidden 추가 */
  overflow: hidden;
}

/* 미리보기 이미지 자체에 대한 스타일 추가 */
.image-preview img {
  width: 100%;
  height: 100%;
  /* 이미지가 비율을 유지하면서 꽉 차도록 object-fit: cover 적용 */
  object-fit: cover;
}
/* --- ▲▲▲ 이미지 관련 보강된 스타일 ▲▲▲ --- */


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

.fields-grid {
  display: grid;                 
  grid-template-columns: 1fr 1fr; 
  column-gap: 1.5rem;   
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