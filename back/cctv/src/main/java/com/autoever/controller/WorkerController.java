package com.autoever.controller;
import com.autoever.model.WorkerModel;
import com.autoever.service.WorkerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/posts")
public class WorkerController {
    private final WorkerService workerService;
    @Autowired
    public WorkerController(WorkerService workerService){
        this.workerService = workerService;
    }

    @GetMapping
    public List<WorkerModel> getAllWorker(){
        return workerService.getAllWorker();
    }

    @GetMapping
    public List<WorkerModel> getTodayWork(String today){
        return workerService.getTodayWork(today);
    }

    @PutMapping
    public int registerWorker(WorkerModel worker, List<String> dates){
        return workerService.registerWorker(worker, dates);
    }

    @PostMapping
    public int modifyWorker(WorkerModel worker, int workerid, List<String> dates){
        return workerService.modifyWorker(worker, workerid, dates);
    }

    @DeleteMapping
    public int deleteWorker(int workerid){
        return workerService.deleteWorker(workerid);
    }

}
