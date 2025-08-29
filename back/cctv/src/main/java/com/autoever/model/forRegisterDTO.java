// WorkerRequest.java
package com.autoever.model;

import java.util.List;

public class forRegisterDTO {
    private WorkerModel worker;
    private Integer workerid;
    private List<String> dates;

    public WorkerModel getWorker() {
        return worker;
    }

    public void setWorker(WorkerModel worker) {
        this.worker = worker;
    }

    // Getter and Setter for workerid
    public Integer getWorkerid() {
        return workerid;
    }

    public void setWorkerid(Integer workerid) {
        this.workerid = workerid;
    }

    // Getter and Setter for dates
    public List<String> getDates() {
        return dates;
    }

    public void setDates(List<String> dates) {
        this.dates = dates;
    }
}