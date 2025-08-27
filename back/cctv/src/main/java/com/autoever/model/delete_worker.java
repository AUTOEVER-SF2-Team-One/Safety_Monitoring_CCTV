package com.autoever.model;

import java.time.LocalDateTime;
//delete to worker model
public class delete_worker {
    private int IDX;
    private int WORKERID;
    private String WORKERRANK;
    private String PHONENUMBER;
    private String PHOTOPATH;
    private int WORKERISDELETE;
    private String WORKER_UPLOAD_DATE;
    private String WORK_DATE;
    public int getIDX(){
        return IDX;
    }

    public void setIDX(int IDX) {
        this.IDX = IDX;
    }

    public int getWORKERID() {
        return WORKERID;
    }

    public void setWORKERID(int WORKERID) {
        this.WORKERID = WORKERID;
    }

    public String getWORKERRANK() {
        return WORKERRANK;
    }

    public void setWORKERRANK(String WORKERRANK) {
        this.WORKERRANK = WORKERRANK;
    }

    public String getPHONENUMBER() {
        return PHONENUMBER;
    }

    public void setPHONENUMBER(String PHONENUMBER) {
        this.PHONENUMBER = PHONENUMBER;
    }

    public String getPHOTOPATH() {
        return PHOTOPATH;
    }

    public void setPHOTOPATH(String PHOTOPATH) {
        this.PHOTOPATH = PHOTOPATH;
    }

    public int getWORKERISDELETE() {
        return WORKERISDELETE;
    }

    public void setWORKERISDELETE(int WORKERISDELETE) {
        this.WORKERISDELETE = WORKERISDELETE;
    }

    public String getWORKER_UPLOAD_DATE() {
        return WORKER_UPLOAD_DATE;
    }

    public void setWORKER_UPLOAD_DATE(String WORKER_UPLOAD_DATE) {
        this.WORKER_UPLOAD_DATE = WORKER_UPLOAD_DATE;
    }

    public String getWORK_DATE() {
        return WORK_DATE;
    }

    public void setWORK_DATE(String WORK_DATE) {
        this.WORK_DATE = WORK_DATE;
    }
}
