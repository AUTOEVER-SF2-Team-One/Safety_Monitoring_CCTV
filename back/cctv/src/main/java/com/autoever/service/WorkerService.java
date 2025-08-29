package com.autoever.service;

import com.autoever.mapper.WorkerMapper;
import com.autoever.model.WorkerModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class WorkerService {
    private final WorkerMapper workerMapper;

    @Autowired
    public WorkerService(WorkerMapper workerMapper) {
        this.workerMapper = workerMapper;
    }

    // 모든 작업자 조회
    public List<WorkerModel> getAllWorkers() {
        List<WorkerModel> workers = workerMapper.findAllWorkers();
        // 각 작업자의 근무 날짜 정보를 설정
        for (WorkerModel worker : workers) {
            worker.setWorkingDates(workerMapper.findWorkingDatesByWorkerId(worker.getId()));
        }
        return workers;
    }

    // ID로 특정 작업자 조회
    public WorkerModel getWorkerById(Long id) {
        WorkerModel worker = workerMapper.findWorkerById(id);
        if (worker != null) {
            worker.setWorkingDates(workerMapper.findWorkingDatesByWorkerId(id));
        }
        return worker;
    }

    // 새로운 작업자 추가
    @Transactional
    public WorkerModel createWorker(WorkerModel worker) {
        // 사원번호 중복 체크
        if (workerMapper.findWorkerByEmployeeId(worker.getEmployeeId()) != null) {
            throw new RuntimeException("이미 존재하는 사원번호입니다: " + worker.getEmployeeId());
        }

        // 작업자 기본 정보 저장
        workerMapper.insertWorker(worker);
        
        // 근무 날짜 정보 저장
        if (worker.getWorkingDates() != null && !worker.getWorkingDates().isEmpty()) {
            for (String date : worker.getWorkingDates()) {
                workerMapper.insertWorkingDate(worker.getId(), date);
            }
        }

        return getWorkerById(worker.getId());
    }

    // 작업자 정보 수정
    @Transactional
    public WorkerModel updateWorker(Long id, WorkerModel worker) {
        // 기존 작업자 존재 여부 확인
        WorkerModel existingWorker = workerMapper.findWorkerById(id);
        if (existingWorker == null) {
            throw new RuntimeException("수정할 작업자를 찾을 수 없습니다. ID: " + id);
        }

        // ID 설정
        worker.setId(id);
        
        // 기존 근무 날짜 삭제
        workerMapper.deleteWorkingDates(id);
        
        // 작업자 정보 수정
        workerMapper.updateWorker(worker);
        
        // 새로운 근무 날짜 추가
        if (worker.getWorkingDates() != null && !worker.getWorkingDates().isEmpty()) {
            for (String date : worker.getWorkingDates()) {
                workerMapper.insertWorkingDate(id, date);
            }
        }

        return getWorkerById(id);
    }

    // 작업자 삭제
    @Transactional
    public boolean deleteWorker(Long id) {
        // 기존 작업자 존재 여부 확인
        WorkerModel existingWorker = workerMapper.findWorkerById(id);
        if (existingWorker == null) {
            throw new RuntimeException("삭제할 작업자를 찾을 수 없습니다. ID: " + id);
        }

        // 근무 날짜 삭제
        workerMapper.deleteWorkingDates(id);
        
        // 작업자 삭제
        return workerMapper.deleteWorker(id) > 0;
    }

    // 사원번호로 작업자 존재 여부 확인
    public boolean existsByEmployeeId(String employeeId) {
        return workerMapper.findWorkerByEmployeeId(employeeId) != null;
    }
}
