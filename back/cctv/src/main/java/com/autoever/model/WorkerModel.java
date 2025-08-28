package com.autoever.model;

//delete to worker model
public class WorkerModel {

    //get from WORKER table
    private int IDX;
    private int WORKERID;
    private String WORKERNAME;
    private String WORKERRANK;
    private String PHONENUMBER;
    private String PHOTOPATH;
    private int WORKERISDELETE;
    private String WORKER_UPLOAD_DATE;
    //get from WORK table
    private int WORKID;
    private String WORK_DATE;

    public int getIDX() {
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

    public String getWORKERNAME() {
        return WORKERNAME;
    }

    public void setWORKERNAME(String WORKERNAME) {
        this.WORKERNAME = WORKERNAME;
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

    public int getWORKID() {
        return WORKID;
    }

    public void setWORKID(int WORKID) {
        this.WORKID = WORKID;
    }

    public String getWORK_DATE() {
        return WORK_DATE;
    }

    public void setWORK_DATE(String WORK_DATE) {
        this.WORK_DATE = WORK_DATE;
    }

}
