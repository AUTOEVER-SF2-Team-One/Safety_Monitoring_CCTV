package com.autoever.util;

import java.util.List;
import java.util.regex.Pattern;

public class ValidationUtil {
    
    // 사원번호 유효성 검사: 영문자, 숫자, 하이픈(-)만 허용, 최대 20자
    private static final Pattern EMPLOYEE_ID_PATTERN = Pattern.compile("^[a-zA-Z0-9-]{1,20}$");
    
    // 이름 유효성 검사: 한글, 영문자, 공백만 허용, 최대 50자
    private static final Pattern NAME_PATTERN = Pattern.compile("^[가-힣a-zA-Z\\s]{1,50}$");
    
    // 직책 유효성 검사: 한글, 영문자, 공백만 허용, 최대 100자
    private static final Pattern POSITION_PATTERN = Pattern.compile("^[가-힣a-zA-Z\\s]{1,100}$");
    
    // 전화번호 유효성 검사: 다양한 전화번호 형식 지원
    private static final Pattern PHONE_PATTERN = Pattern.compile("^[+]?[0-9\\s\\(\\)\\-]{7,20}$");
    
    // 날짜 형식 검사: YYYY-MM-DD
    private static final Pattern DATE_PATTERN = Pattern.compile("^\\d{4}-\\d{2}-\\d{2}$");

    /**
     * 사원번호 유효성 검사
     */
    public static boolean isValidEmployeeId(String employeeId) {
        if (employeeId == null || employeeId.trim().isEmpty()) {
            return false;
        }
        return EMPLOYEE_ID_PATTERN.matcher(employeeId.trim()).matches();
    }

    /**
     * 이름 유효성 검사
     */
    public static boolean isValidName(String name) {
        if (name == null || name.trim().isEmpty()) {
            return false;
        }
        return NAME_PATTERN.matcher(name.trim()).matches();
    }

    /**
     * 직책 유효성 검사
     */
    public static boolean isValidPosition(String position) {
        if (position == null || position.trim().isEmpty()) {
            return false;
        }
        return POSITION_PATTERN.matcher(position.trim()).matches();
    }

    /**
     * 전화번호 유효성 검사
     */
    public static boolean isValidPhone(String phone) {
        if (phone == null || phone.trim().isEmpty()) {
            return false;
        }
        return PHONE_PATTERN.matcher(phone.trim()).matches();
    }

    /**
     * 날짜 형식 유효성 검사
     */
    public static boolean isValidDate(String date) {
        if (date == null || date.trim().isEmpty()) {
            return false;
        }
        return DATE_PATTERN.matcher(date.trim()).matches();
    }

    /**
     * 근무 날짜 목록 유효성 검사
     */
    public static boolean isValidWorkingDates(List<String> workingDates) {
        if (workingDates == null) {
            return true; // null은 허용
        }
        
        for (String date : workingDates) {
            if (!isValidDate(date)) {
                return false;
            }
        }
        return true;
    }

    /**
     * 이미지 URL 유효성 검사
     */
    public static boolean isValidImageUrl(String imageUrl) {
        if (imageUrl == null) {
            return true; // null은 허용
        }
        
        if (imageUrl.trim().isEmpty()) {
            return false;
        }
        
        // 간단한 URL 형식 검사
        return imageUrl.startsWith("http://") || imageUrl.startsWith("https://") || imageUrl.startsWith("/");
    }

    /**
     * 전체 Worker 모델 유효성 검사
     */
    public static ValidationResult validateWorker(com.autoever.model.WorkerModel worker) {
        ValidationResult result = new ValidationResult();
        
        if (!isValidEmployeeId(worker.getEmployeeId())) {
            result.addError("사원번호는 영문자, 숫자, 하이픈(-)만 허용되며 최대 20자까지 입력 가능합니다.");
        }
        
        if (!isValidName(worker.getName())) {
            result.addError("이름은 한글, 영문자, 공백만 허용되며 최대 50자까지 입력 가능합니다.");
        }
        
        if (!isValidPosition(worker.getPosition())) {
            result.addError("직책은 한글, 영문자, 공백만 허용되며 최대 100자까지 입력 가능합니다.");
        }
        
        if (!isValidPhone(worker.getPhone())) {
            result.addError("전화번호 형식이 올바르지 않습니다.");
        }
        
        if (!isValidWorkingDates(worker.getWorkingDates())) {
            result.addError("근무 날짜는 YYYY-MM-DD 형식으로 입력해야 합니다.");
        }
        
        if (!isValidImageUrl(worker.getImage())) {
            result.addError("이미지 URL 형식이 올바르지 않습니다.");
        }
        
        return result;
    }

    /**
     * 유효성 검사 결과를 담는 클래스
     */
    public static class ValidationResult {
        private final java.util.List<String> errors = new java.util.ArrayList<>();
        
        public void addError(String error) {
            errors.add(error);
        }
        
        public boolean isValid() {
            return errors.isEmpty();
        }
        
        public java.util.List<String> getErrors() {
            return new java.util.ArrayList<>(errors);
        }
        
        public String getFirstError() {
            return errors.isEmpty() ? null : errors.get(0);
        }
    }
}
