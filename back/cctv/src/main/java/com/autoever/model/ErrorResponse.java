package com.autoever.model;

import java.time.LocalDateTime;

public class ErrorResponse {
    private String timestamp;           // 에러 발생 시간
    private int status;                 // HTTP 상태 코드
    private String error;               // 에러 타입
    private String message;             // 사용자 친화적 메시지
    private String details;             // 상세 에러 정보

    // 기본 생성자
    public ErrorResponse() {
        this.timestamp = LocalDateTime.now().toString();
    }

    // 전체 필드 생성자
    public ErrorResponse(int status, String error, String message, String details) {
        this();
        this.status = status;
        this.error = error;
        this.message = message;
        this.details = details;
    }

    // Getter와 Setter
    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public int getStatus() {
        return status;
    }

    public void setStatus(int status) {
        this.status = status;
    }

    public String getError() {
        return error;
    }

    public void setError(String error) {
        this.error = error;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getDetails() {
        return details;
    }

    public void setDetails(String details) {
        this.details = details;
    }

    @Override
    public String toString() {
        return "ErrorResponse{" +
                "timestamp='" + timestamp + '\'' +
                ", status=" + status +
                ", error='" + error + '\'' +
                ", message='" + message + '\'' +
                ", details='" + details + '\'' +
                '}';
    }
}
