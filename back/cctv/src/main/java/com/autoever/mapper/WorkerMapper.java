package com.autoever.mapper;

import com.autoever.model.WorkerModel;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface WorkerMapper {
    // 모든 작업자 조회
    List<WorkerModel> findAllWorkers();
    
    // ID로 특정 작업자 조회
    WorkerModel findWorkerById(@Param("id") Long id);
    
    // 사원번호로 작업자 조회 (중복 체크용)
    WorkerModel findWorkerByEmployeeId(@Param("employeeId") String employeeId);
    
    // 새로운 작업자 추가
    int insertWorker(WorkerModel worker);
    
    // 작업자 정보 수정
    int updateWorker(WorkerModel worker);
    
    // 작업자 삭제
    int deleteWorker(@Param("id") Long id);
    
    // 근무 날짜 추가
    int insertWorkingDate(@Param("workerId") Long workerId, @Param("date") String date);
    
    // 근무 날짜 삭제
    int deleteWorkingDates(@Param("workerId") Long workerId);
    
    // 근무 날짜 조회
    List<String> findWorkingDatesByWorkerId(@Param("workerId") Long workerId);
}
