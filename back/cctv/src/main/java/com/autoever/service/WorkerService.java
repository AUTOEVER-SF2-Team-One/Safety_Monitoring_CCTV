package com.autoever.service;

import com.autoever.mapper.WorkerMapper;
import com.autoever.model.WorkerModel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class WorkerService {
    private final WorkerMapper workerMapper;

    @Autowired
    public WorkerService(WorkerMapper workerMapper) {
        this.workerMapper = workerMapper;
    }
    //check worker
    public List<WorkerModel> getAllWorker(){
        return workerMapper.findAllWorker();
    }
    public List<WorkerModel> getTodayWork(String today_date){
        return workerMapper.findTodayWork(today_date);
    }

    //register worker
    public int registerWorker(WorkerModel worker, List<String> dates){
        workerMapper.insertWorker(worker);
        for(String date : dates){
            worker.setWORK_DATE(date);
            workerMapper.insertWork(worker);
        }
        return 1;
    }

    //modify worker
    public int modifyWorker(WorkerModel worker, int workerid, List<String> dates){
        workerMapper.deleteWorker(workerid);
        workerMapper.deleteWork(workerid);
        return registerWorker(worker, dates);
    }

    //delete worker
    public int deleteWorker(int workerid){
        workerMapper.deleteWork(workerid);
        return workerMapper.deleteWorker(workerid);
    }
}
