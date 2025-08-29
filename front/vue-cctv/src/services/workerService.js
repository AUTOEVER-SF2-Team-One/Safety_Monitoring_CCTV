import api from './api.js';

/**
 * 작업자 정보 CRUD API 서비스
 */
export const workerService = {
  /**
   * 모든 작업자 목록 조회
   * @returns {Promise<Array>} 작업자 목록
   */
  async getAllWorkers() {
    try {
      const response = await api.get('/api/workers');
      return response.data;
    } catch (error) {
      console.error('작업자 목록 조회 실패:', error);
      throw error;
    }
  },

  /**
   * 특정 작업자 조회
   * @param {number} id - 작업자 ID
   * @returns {Promise<Object>} 작업자 정보
   */
  async getWorkerById(id) {
    try {
      const response = await api.get(`/api/workers/${id}`);
      return response.data;
    } catch (error) {
      console.error('작업자 조회 실패:', error);
      throw error;
    }
  },

  /**
   * 새로운 작업자 추가
   * @param {Object} workerData - 작업자 정보
   * @returns {Promise<Object>} 생성된 작업자 정보
   */
  async createWorker(workerData) {
    try {
      const response = await api.post('/api/workers', workerData);
      return response.data;
    } catch (error) {
      console.error('작업자 생성 실패:', error);
      throw error;
    }
  },

  /**
   * 작업자 정보 수정
   * @param {number} id - 작업자 ID
   * @param {Object} workerData - 수정할 작업자 정보
   * @returns {Promise<Object>} 수정된 작업자 정보
   */
  async updateWorker(id, workerData) {
    try {
      const response = await api.put(`/api/workers/${id}`, workerData);
      return response.data;
    } catch (error) {
      console.error('작업자 수정 실패:', error);
      throw error;
    }
  },

  /**
   * 작업자 삭제
   * @param {number} id - 작업자 ID
   * @returns {Promise<void>}
   */
  async deleteWorker(id) {
    try {
      await api.delete(`/api/workers/${id}`);
    } catch (error) {
      console.error('작업자 삭제 실패:', error);
      throw error;
    }
  }
};
