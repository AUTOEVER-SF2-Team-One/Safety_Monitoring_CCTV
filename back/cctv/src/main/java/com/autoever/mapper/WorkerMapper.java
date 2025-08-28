package com.autoever.mapper;

import com.autoever.model.WorkerModel;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface WorkerMapper {
    //Worker information list findAll
    List<WorkerModel> findAllWorker();
    //Work informaion list Today
    List<WorkerModel> findTodayWork(String today_date);
    //Worker information register
    int insertWorker(WorkerModel worker);
    //Work information register
    int insertWork(WorkerModel worker);
    //Worker information update
    int updateWorker(WorkerModel worker);
    //Work information update
    int deleteForUpdateDate(@Param("workerid") int workerid);
    //Worker information delete
    int deleteWorker(@Param("WORKERID") int workerid);
    //Work informaion delete
    int deleteWork(@Param("WORKERID") int workerid);


}
