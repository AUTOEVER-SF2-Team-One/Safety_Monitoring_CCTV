# 작업자 관리 API 명세서

## 개요
CCTV 안전 모니터링 시스템의 작업자 정보를 관리하는 REST API입니다.

## 기본 정보
- **Base URL**: `http://localhost:8080`
- **Content-Type**: `application/json`
- **API 경로**: `/workers`
- **CORS**: 프론트엔드(`http://localhost:5173`)에서 접근 허용

## API 엔드포인트

### 1. 모든 작업자 조회

#### 요청
```http
GET /workers
```

#### 응답
**성공 (200 OK)**
```json
[
  {
    "id": 1,
    "employeeId": "201902927",
    "name": "Sarah Johnson",
    "position": "Safety Inspector",
    "phone": "+1(555) 987-6543",
    "workingDates": ["2025-08-22", "2025-08-23", "2025-08-25"],
    "image": null
  },
  {
    "id": 2,
    "employeeId": "202011234",
    "name": "Daniel Kim",
    "position": "Safety Inspector",
    "phone": "+1(555) 987-6543",
    "workingDates": ["2025-09-01", "2025-09-02"],
    "image": null
  }
]
```

**에러 (500 Internal Server Error)**
```json
{
  "timestamp": "2025-01-15T10:30:00.000+00:00",
  "status": 500,
  "error": "Internal Server Error",
  "message": "서버 내부 오류가 발생했습니다.",
  "details": "데이터베이스 연결 실패"
}
```

---

### 2. 특정 작업자 조회

#### 요청
```http
GET /workers/{id}
```

**Path Parameters:**
- `id` (Long): 작업자 고유 식별자

#### 응답
**성공 (200 OK)**
```json
{
  "id": 1,
  "employeeId": "201902927",
  "name": "Sarah Johnson",
  "position": "Safety Inspector",
  "phone": "+1(555) 987-6543",
  "workingDates": ["2025-08-22", "2025-08-23", "2025-08-25"],
  "image": null
}
```

**에러 (404 Not Found)**
```json
{
  "timestamp": "2025-01-15T10:30:00.000+00:00",
  "status": 404,
  "error": "Not Found",
  "message": "요청한 작업자를 찾을 수 없습니다.",
  "details": "ID: 999인 작업자가 존재하지 않습니다."
}
```

---

### 3. 새로운 작업자 추가

#### 요청
```http
POST /workers
Content-Type: application/json
```

**Request Body:**
```json
{
  "employeeId": "202312345",
  "name": "홍길동",
  "position": "Safety Inspector",
  "phone": "010-1234-5678",
  "workingDates": ["2025-01-15", "2025-01-16"],
  "image": null
}
```

**필드 설명:**
- `employeeId` (String, 필수): 사원번호 (고유값)
- `name` (String, 필수): 작업자 이름
- `position` (String, 필수): 직책
- `phone` (String, 필수): 전화번호
- `workingDates` (Array<String>, 선택): 근무 날짜 목록 (YYYY-MM-DD 형식)
- `image` (String, 선택): 프로필 이미지 URL (null 가능)

#### 응답
**성공 (201 Created)**
```json
{
  "id": 3,
  "employeeId": "202312345",
  "name": "홍길동",
  "position": "Safety Inspector",
  "phone": "010-1234-5678",
  "workingDates": ["2025-01-15", "2025-01-16"],
  "image": null
}
```

**에러 (400 Bad Request) - 유효성 검사 실패**
```json
{
  "timestamp": "2025-01-15T10:30:00.000+00:00",
  "status": 400,
  "error": "Bad Request",
  "message": "입력 데이터가 유효하지 않습니다.",
  "details": [
    "이름은 필수 입력 항목입니다.",
    "사원번호는 이미 존재합니다."
  ]
}
```

**에러 (409 Conflict) - 중복 사원번호**
```json
{
  "timestamp": "2025-01-15T10:30:00.000+00:00",
  "status": 409,
  "error": "Conflict",
  "message": "이미 존재하는 사원번호입니다.",
  "details": "사원번호 202312345는 이미 등록되어 있습니다."
}
```

---

### 4. 작업자 정보 수정

#### 요청
```http
PUT /workers/{id}
Content-Type: application/json
```

**Path Parameters:**
- `id` (Long): 수정할 작업자 고유 식별자

**Request Body:**
```json
{
  "name": "Sarah Johnson Updated",
  "position": "Senior Safety Inspector",
  "phone": "+1(555) 999-8888"
}
```

**참고:** 부분 업데이트 지원. 전송되지 않은 필드는 기존 값 유지

#### 응답
**성공 (200 OK)**
```json
{
  "id": 1,
  "employeeId": "201902927",
  "name": "Sarah Johnson Updated",
  "position": "Senior Safety Inspector",
  "phone": "+1(555) 999-8888",
  "workingDates": ["2025-08-22", "2025-08-23", "2025-08-25"],
  "image": null
}
```

**에러 (404 Not Found)**
```json
{
  "timestamp": "2025-01-15T10:30:00.000+00:00",
  "status": 404,
  "error": "Not Found",
  "message": "수정할 작업자를 찾을 수 없습니다.",
  "details": "ID: 999인 작업자가 존재하지 않습니다."
}
```

**에러 (400 Bad Request) - 유효성 검사 실패**
```json
{
  "timestamp": "2025-01-15T10:30:00.000+00:00",
  "status": 400,
  "error": "Bad Request",
  "message": "입력 데이터가 유효하지 않습니다.",
  "details": "전화번호 형식이 올바르지 않습니다."
}
```

---

### 5. 작업자 삭제

#### 요청
```http
DELETE /workers/{id}
```

**Path Parameters:**
- `id` (Long): 삭제할 작업자 고유 식별자

#### 응답
**성공 (204 No Content)**
응답 본문 없음

**성공 (200 OK) - 삭제 확인 메시지**
```json
{
  "message": "작업자가 성공적으로 삭제되었습니다.",
  "deletedId": 1
}
```

**에러 (404 Not Found)**
```json
{
  "timestamp": "2025-01-15T10:30:00.000+00:00",
  "status": 404,
  "error": "Not Found",
  "message": "삭제할 작업자를 찾을 수 없습니다.",
  "details": "ID: 999인 작업자가 존재하지 않습니다."
}
```

---

## 데이터 모델

### Worker 엔티티
```java
public class Worker {
    private Long id;                    // 고유 식별자 (자동 생성)
    private String employeeId;          // 사원번호 (고유값, 필수)
    private String name;                // 이름 (필수)
    private String position;            // 직책 (필수)
    private String phone;               // 전화번호 (필수)
    private List<String> workingDates; // 근무 날짜 목록 (선택)
    private String image;               // 프로필 이미지 URL (선택)
    
    // 생성자, getter, setter
}
```

### 에러 응답 모델
```java
public class ErrorResponse {
    private String timestamp;           // 에러 발생 시간
    private int status;                 // HTTP 상태 코드
    private String error;               // 에러 타입
    private String message;             // 사용자 친화적 메시지
    private String details;             // 상세 에러 정보
    
    // 생성자, getter, setter
}
```

---

## 유효성 검사 규칙

### 필수 필드
- `employeeId`: null이 아니고 빈 문자열이 아니어야 함
- `name`: null이 아니고 빈 문자열이 아니어야 함
- `position`: null이 아니고 빈 문자열이 아니어야 함
- `phone`: null이 아니고 빈 문자열이 아니어야 함

### 데이터 형식
- `employeeId`: 영문자, 숫자, 하이픈(-)만 허용, 최대 20자
- `name`: 한글, 영문자, 공백만 허용, 최대 50자
- `position`: 한글, 영문자, 공백만 허용, 최대 100자
- `phone`: 전화번호 형식 (010-1234-5678, +1(555) 123-4567 등)
- `workingDates`: YYYY-MM-DD 형식의 문자열 배열
- `image`: 유효한 URL 형식 또는 null

### 비즈니스 규칙
- `employeeId`는 시스템 내에서 고유해야 함
- `workingDates`는 과거 날짜만 허용
- 삭제된 작업자의 `employeeId`는 재사용 가능

---

## HTTP 상태 코드

| 상태 코드 | 설명 | 사용 사례 |
|-----------|------|-----------|
| 200 | OK | GET, PUT 요청 성공 |
| 201 | Created | POST 요청 성공 (새 리소스 생성) |
| 204 | No Content | DELETE 요청 성공 |
| 400 | Bad Request | 요청 데이터 유효성 검사 실패 |
| 404 | Not Found | 요청한 리소스를 찾을 수 없음 |
| 409 | Conflict | 리소스 충돌 (중복 사원번호 등) |
| 500 | Internal Server Error | 서버 내부 오류 |

---

## CORS 설정

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins("http://localhost:5173") // Vue.js 개발 서버
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true);
    }
}
```

---

## 테스트 시나리오

### 1. 정상 케이스
- 빈 데이터베이스에서 첫 번째 작업자 추가
- 기존 작업자 정보 수정
- 작업자 삭제 후 목록 확인

### 2. 에러 케이스
- 존재하지 않는 ID로 조회/수정/삭제
- 중복된 사원번호로 추가
- 필수 필드 누락으로 추가/수정
- 잘못된 데이터 형식으로 추가/수정

### 3. 경계값 테스트
- 매우 긴 이름/직책 입력
- 빈 문자열 입력
- null 값 입력
- 특수문자 포함 입력

---

## 구현 시 주의사항

1. **트랜잭션 관리**: 데이터 일관성을 위해 적절한 트랜잭션 경계 설정
2. **로깅**: 모든 API 호출과 에러 상황에 대한 적절한 로깅
3. **보안**: 입력 데이터 검증 및 SQL 인젝션 방지
4. **성능**: 대용량 데이터 처리 시 페이징 고려
5. **모니터링**: API 응답 시간 및 에러율 모니터링
