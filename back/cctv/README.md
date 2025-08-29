# CCTV 안전 모니터링 시스템 - 백엔드

## 개요
CCTV 안전 모니터링 시스템의 작업자 정보를 관리하는 Spring Boot 백엔드 애플리케이션입니다.

## 기술 스택
- **Java 17**
- **Spring Boot 3.5.5**
- **MyBatis 3.0.5**
- **MySQL Database** (localhost:3306)
- **Maven**

## 프로젝트 구조
```
src/main/java/com/autoever/
├── config/
│   └── WebConfig.java              # CORS 설정
├── controller/
│   └── WorkerController.java       # 작업자 관리 REST API
├── mapper/
│   └── WorkerMapper.java           # MyBatis 매퍼 인터페이스
├── model/
│   ├── WorkerModel.java            # 작업자 모델
│   └── ErrorResponse.java          # 에러 응답 모델
├── service/
│   └── WorkerService.java          # 비즈니스 로직
└── util/
    └── ValidationUtil.java         # 유효성 검사 유틸리티

src/main/resources/
├── mapper/
│   └── WorkerMapper.xml            # MyBatis SQL 매퍼
├── data.sql                        # 초기 데이터
└── application.properties          # 애플리케이션 설정
```

## API 엔드포인트

### 작업자 관리
- `GET /workers` - 모든 작업자 조회
- `GET /workers/{id}` - 특정 작업자 조회
- `POST /workers` - 새로운 작업자 추가
- `PUT /workers/{id}` - 작업자 정보 수정
- `DELETE /workers/{id}` - 작업자 삭제

## 실행 방법

### 1. 사전 요구사항
- Java 17 이상
- Maven 3.6 이상
- MySQL 8.0 이상 (localhost:3306에서 실행 중)

### 2. 프로젝트 빌드
```bash
cd back/cctv
mvn clean compile
```

### 3. MySQL 데이터베이스 설정
```bash
# MySQL에 연결
mysql -u root -p

# 데이터베이스 생성 스크립트 실행
source create_mysql_db.sql
```

### 4. 애플리케이션 실행
```bash
mvn spring-boot:run
```

### 5. 접속 확인
- 애플리케이션: http://localhost:8080
- MySQL 데이터베이스: localhost:3306/cctv_db

## 데이터베이스 스키마

### workers 테이블
- `id`: 고유 식별자 (자동 증가)
- `employee_id`: 사원번호 (고유값, 필수)
- `name`: 이름 (필수)
- `position`: 직책 (필수)
- `phone`: 전화번호 (필수)
- `image`: 프로필 이미지 URL (선택)

### working_dates 테이블
- `id`: 고유 식별자 (자동 증가)
- `worker_id`: 작업자 ID (외래키)
- `work_date`: 근무 날짜 (YYYY-MM-DD 형식)

## CORS 설정
프론트엔드(`http://localhost:5173`)에서의 접근을 허용합니다.

## 유효성 검사 규칙

### 필수 필드
- `employeeId`: 영문자, 숫자, 하이픈(-)만 허용, 최대 20자
- `name`: 한글, 영문자, 공백만 허용, 최대 50자
- `position`: 한글, 영문자, 공백만 허용, 최대 100자
- `phone`: 전화번호 형식 (010-1234-5678, +1(555) 123-4567 등)

### 선택 필드
- `workingDates`: YYYY-MM-DD 형식의 문자열 배열
- `image`: 유효한 URL 형식 또는 null

## 에러 처리
모든 API는 표준화된 에러 응답 형식을 제공합니다:

```json
{
  "timestamp": "2025-01-15T10:30:00.000+00:00",
  "status": 400,
  "error": "Bad Request",
  "message": "입력 데이터가 유효하지 않습니다.",
  "details": "상세 에러 정보"
}
```

## 개발 환경 설정

### 로깅 레벨
- `com.autoever`: DEBUG
- `org.springframework.web`: DEBUG

### SQL 로깅
- MyBatis SQL 쿼리 로깅 활성화
- SQL 포맷팅 활성화

## 테스트
```bash
mvn test
```

## 빌드
```bash
mvn clean package
```

## 배포
```bash
java -jar target/cctv-0.0.1-SNAPSHOT.jar
```
