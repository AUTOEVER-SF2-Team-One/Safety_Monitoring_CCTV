package com.autoever.model;

import java.util.List;

//put to worker model
public class put_worker {
    private int WORKERID;
    private String WORKERNAME;
    private String WORKERRANK;
    private String PHONENUMBER;
    private List<String> WORKERDATE;
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

    public List<String> getWORKERDATE() {
        return WORKERDATE;
    }

    public void setWORKERDATE(List<String> WORKERDATE) {
        this.WORKERDATE = WORKERDATE;
    }
}
