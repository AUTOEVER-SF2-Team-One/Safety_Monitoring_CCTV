<template>
  <div class="api-test-container">
    <h1>API 테스트 페이지</h1>
    
    <div class="test-section">
      <h2>작업자 API 테스트</h2>
      
      <!-- GET /workers 테스트 -->
      <div class="test-item">
        <h3>GET /workers - 모든 작업자 조회</h3>
        <button @click="testGetAllWorkers" :disabled="isLoading">작업자 목록 조회</button>
        <div v-if="getAllResult" class="result">
          <h4>결과:</h4>
          <pre>{{ JSON.stringify(getAllResult, null, 2) }}</pre>
        </div>
      </div>

      <!-- POST /workers 테스트 -->
      <div class="test-item">
        <h3>POST /workers - 작업자 추가</h3>
        <div class="form-group">
          <label>사원번호:</label>
          <input v-model="newWorker.employeeId" placeholder="사원번호 입력" />
        </div>
        <div class="form-group">
          <label>이름:</label>
          <input v-model="newWorker.name" placeholder="이름 입력" />
        </div>
        <div class="form-group">
          <label>직책:</label>
          <input v-model="newWorker.position" placeholder="직책 입력" />
        </div>
        <div class="form-group">
          <label>전화번호:</label>
          <input v-model="newWorker.phone" placeholder="전화번호 입력" />
        </div>
        <button @click="testCreateWorker" :disabled="isLoading">작업자 추가</button>
        <div v-if="createResult" class="result">
          <h4>결과:</h4>
          <pre>{{ JSON.stringify(createResult, null, 2) }}</pre>
        </div>
      </div>

      <!-- PUT /workers/{id} 테스트 -->
      <div class="test-item">
        <h3>PUT /workers/{id} - 작업자 수정</h3>
        <div class="form-group">
          <label>수정할 작업자 ID:</label>
          <input v-model="updateWorkerId" type="number" placeholder="ID 입력" />
        </div>
        <div class="form-group">
          <label>새 이름:</label>
          <input v-model="updateWorkerData.name" placeholder="새 이름 입력" />
        </div>
        <button @click="testUpdateWorker" :disabled="isLoading">작업자 수정</button>
        <div v-if="updateResult" class="result">
          <h4>결과:</h4>
          <pre>{{ JSON.stringify(updateResult, null, 2) }}</pre>
        </div>
      </div>

      <!-- DELETE /workers/{id} 테스트 -->
      <div class="test-item">
        <h3>DELETE /workers/{id} - 작업자 삭제</h3>
        <div class="form-group">
          <label>삭제할 작업자 ID:</label>
          <input v-model="deleteWorkerId" type="number" placeholder="ID 입력" />
        </div>
        <button @click="testDeleteWorker" :disabled="isLoading">작업자 삭제</button>
        <div v-if="deleteResult" class="result">
          <h4>결과:</h4>
          <pre>{{ deleteResult }}</pre>
        </div>
      </div>
    </div>

    <!-- 로딩 표시 -->
    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>처리 중...</p>
    </div>

    <!-- 에러 메시지 -->
    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { workerService } from '@/services/workerService.js';

// 상태 관리
const isLoading = ref(false);
const errorMessage = ref('');

// 테스트 결과
const getAllResult = ref(null);
const createResult = ref(null);
const updateResult = ref(null);
const deleteResult = ref(null);

// 폼 데이터
const newWorker = ref({
  employeeId: '',
  name: '',
  position: '',
  phone: '',
  workingDates: []
});

const updateWorkerId = ref('');
const updateWorkerData = ref({
  name: ''
});

const deleteWorkerId = ref('');

// 에러 처리 함수
const handleError = (error, operation) => {
  console.error(`${operation} 실패:`, error);
  errorMessage.value = `${operation}에 실패했습니다: ${error.response?.data?.message || error.message}`;
  setTimeout(() => {
    errorMessage.value = '';
  }, 5000);
};

// GET /workers 테스트
const testGetAllWorkers = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';
    const result = await workerService.getAllWorkers();
    getAllResult.value = result;
  } catch (error) {
    handleError(error, '작업자 목록 조회');
  } finally {
    isLoading.value = false;
  }
};

// POST /workers 테스트
const testCreateWorker = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';
    const result = await workerService.createWorker(newWorker.value);
    createResult.value = result;
    // 폼 초기화
    newWorker.value = {
      employeeId: '',
      name: '',
      position: '',
      phone: '',
      workingDates: []
    };
  } catch (error) {
    handleError(error, '작업자 추가');
  } finally {
    isLoading.value = false;
  }
};

// PUT /workers/{id} 테스트
const testUpdateWorker = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';
    const result = await workerService.updateWorker(updateWorkerId.value, updateWorkerData.value);
    updateResult.value = result;
  } catch (error) {
    handleError(error, '작업자 수정');
  } finally {
    isLoading.value = false;
  }
};

// DELETE /workers/{id} 테스트
const testDeleteWorker = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = '';
    await workerService.deleteWorker(deleteWorkerId.value);
    deleteResult.value = '작업자가 성공적으로 삭제되었습니다.';
    deleteWorkerId.value = '';
  } catch (error) {
    handleError(error, '작업자 삭제');
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.api-test-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.test-section {
  margin-bottom: 40px;
}

.test-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #f9f9f9;
}

.test-item h3 {
  margin-top: 0;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: inline-block;
  width: 120px;
  font-weight: bold;
}

.form-group input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 200px;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

button:hover {
  background-color: #0056b3;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.result {
  margin-top: 15px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
  border-left: 4px solid #007bff;
}

.result h4 {
  margin-top: 0;
  color: #495057;
}

.result pre {
  background-color: #e9ecef;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}

.loading {
  text-align: center;
  padding: 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 4px;
  margin: 20px 0;
  border: 1px solid #f5c6cb;
}
</style>
