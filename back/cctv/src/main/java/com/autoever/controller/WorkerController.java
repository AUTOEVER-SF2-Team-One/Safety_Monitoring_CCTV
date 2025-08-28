package com.autoever.controller;
import com.autoever.model.WorkerModel;
import com.autoever.service.WorkerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/worker")
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

    @GetMapping("/{today}")
    public List<WorkerModel> getTodayWork(@PathVariable String today){
        return workerService.getTodayWork(today);
    }

    @PostMapping
    public int modifyWorker(WorkerModel worker,  @RequestParam(required = false) Integer workerid, @RequestParam List<String> dates){
        return workerService.modifyWorker(worker, workerid, dates);
    }

    @PutMapping
    public int registerWorker(WorkerModel worker, List<String> dates){
        return workerService.registerWorker(worker, dates);
    }

    @DeleteMapping
    public int deleteWorker(@RequestBody int workerid){
        return workerService.deleteWorker(workerid);
    }

}
