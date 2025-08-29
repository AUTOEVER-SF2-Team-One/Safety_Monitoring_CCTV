# 환경 설정 및 사용법

## 환경변수 설정

이 프로젝트는 환경별로 다른 설정을 사용할 수 있도록 환경변수를 지원합니다.

### 환경변수 파일들

- `.env`: 기본 환경변수 (모든 환경에서 공통)
- `.env.development`: 개발 환경 전용 설정
- `.env.production`: 프로덕션 환경 전용 설정

### 주요 환경변수

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `VITE_APP_TITLE` | 애플리케이션 제목 | CCTV 안전 모니터링 시스템 |
| `VITE_API_BASE_URL` | API 서버 기본 URL | http://localhost:8080 |
| `VITE_API_TIMEOUT` | API 요청 타임아웃 (ms) | 10000 |
| `VITE_SERVER_PORT` | 개발 서버 포트 | 5173 |
| `VITE_SERVER_HOST` | 개발 서버 호스트 | localhost |

## 실행 방법

### 개발 서버 시작
```bash
npm run dev
```

### 빌드

#### 개발 환경 빌드
```bash
npm run build:dev
```

#### 프로덕션 환경 빌드
```bash
npm run build:prod
```

#### 기본 빌드
```bash
npm run build
```

### 프리뷰
```bash
npm run preview
```

## CORS 문제 해결

이 프로젝트는 Vite의 프록시 기능을 사용하여 CORS 문제를 해결합니다:

- 개발 환경에서는 `/api` 경로로 요청을 보내면 자동으로 Spring Boot 서버로 프록시됩니다
- 프로덕션 환경에서는 직접 API 서버로 요청합니다

## 환경별 설정

### 개발 환경
- API 서버: http://localhost:8080
- 프록시 사용: 예
- 디버그 모드: 활성화

### 프로덕션 환경
- API 서버: https://your-production-domain.com
- 프록시 사용: 아니오
- 디버그 모드: 비활성화

## 문제 해결

### 환경변수가 적용되지 않는 경우
1. 환경변수 파일이 올바른 위치에 있는지 확인
2. Vite 서버를 재시작
3. 브라우저 캐시 삭제

### CORS 오류가 발생하는 경우
1. Spring Boot 서버가 실행 중인지 확인
2. 프록시 설정이 올바른지 확인
3. 환경변수 `VITE_API_BASE_URL`이 올바르게 설정되었는지 확인
