package com.autoever.model;

import java.util.List;

public class WorkerModel {
    private Long id;                    // 고유 식별자 (자동 생성)
    private String employeeId;          // 사원번호 (고유값, 필수)
    private String name;                // 이름 (필수)
    private String position;            // 직책 (필수)
    private String phone;               // 전화번호 (필수)
    private List<String> workingDates; // 근무 날짜 목록 (선택)
    private String image;               // 프로필 이미지 URL (선택)

    // 기본 생성자
    public WorkerModel() {}

    // 전체 필드 생성자
    public WorkerModel(String employeeId, String name, String position, String phone, List<String> workingDates, String image) {
        this.employeeId = employeeId;
        this.name = name;
        this.position = position;
        this.phone = phone;
        this.workingDates = workingDates;
        this.image = image;
    }

    // Getter와 Setter
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getEmployeeId() {
        return employeeId;
    }

    public void setEmployeeId(String employeeId) {
        this.employeeId = employeeId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPosition() {
        return position;
    }

    public void setPosition(String position) {
        this.position = position;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public List<String> getWorkingDates() {
        return workingDates;
    }

    public void setWorkingDates(List<String> workingDates) {
        this.workingDates = workingDates;
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }

    @Override
    public String toString() {
        return "WorkerModel{" +
                "id=" + id +
                ", employeeId='" + employeeId + '\'' +
                ", name='" + name + '\'' +
                ", position='" + position + '\'' +
                ", phone='" + phone + '\'' +
                ", workingDates=" + workingDates +
                ", image='" + image + '\'' +
                '}';
    }
}
