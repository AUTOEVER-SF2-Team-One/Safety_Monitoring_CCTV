package com.autoever.controller;
import com.autoever.model.WorkerModel;
import com.autoever.model.forRegisterDTO;
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
    public int modifyWorker(@RequestBody forRegisterDTO request){
        return workerService.modifyWorker(
                request.getWorker(),
                request.getWorkerid(),
                request.getDates()
        );
    }

    @PutMapping
    public int registerWorker(@RequestBody forRegisterDTO request){
        return workerService.registerWorker(request.getWorker(),
                request.getDates());
    }

    @DeleteMapping
    public int deleteWorker(@RequestBody int workerid){
        return workerService.deleteWorker(workerid);
    }

}
