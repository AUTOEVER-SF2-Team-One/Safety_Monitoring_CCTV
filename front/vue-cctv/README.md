# CCTV 안전 모니터링 시스템 - 프론트엔드

## 개요
CCTV 안전 모니터링 시스템의 작업자 정보를 관리하는 Vue.js 프론트엔드 애플리케이션입니다.

## 기술 스택
- **Vue 3.5.18**
- **Vite 7.0.6**
- **Vue Router 4.5.1**
- **Pinia 3.0.3**
- **Axios 1.11.0**
- **Node.js 20.19.0+**

## 프로젝트 구조
```
src/
├── components/
│   └── worker/           # 작업자 관련 컴포넌트
│       ├── WorkerCard.vue
│       ├── WorkerForm.vue
│       └── WorkerList.vue
├── views/                # 페이지 뷰
│   ├── ApiTestView.vue
│   └── WorkerManagementView.vue
├── services/             # API 서비스
│   ├── api.js
│   └── workerService.js
├── stores/               # 상태 관리
│   └── counter.js
├── router/               # 라우팅 설정
│   └── index.js
├── App.vue               # 메인 앱 컴포넌트
└── main.js               # 앱 진입점
```

## 개발 서버 설정

### 포트 고정
프론트엔드는 **항상 `http://localhost:5173`에서 실행**됩니다.

- **개발 서버**: `http://localhost:5173`
- **백엔드 API**: `http://localhost:8080`
- **CORS**: 백엔드에서 `http://localhost:5173` 접근 허용

### 설정 파일
- `vite.config.js`: 포트 5173으로 고정
- `package.json`: dev 스크립트에 포트 명시

## 실행 방법

### 1. 사전 요구사항
- Node.js 20.19.0 이상
- npm 또는 yarn

### 2. 의존성 설치
```bash
cd front/vue-cctv
npm install
```

### 3. 개발 서버 실행
```bash
npm run dev
```

**자동으로 `http://localhost:5173`에서 실행됩니다.**

### 4. 빌드
```bash
npm run build
```

### 5. 프리뷰 (빌드된 파일)
```bash
npm run preview
```

## API 연동

### 백엔드 연결
- **Base URL**: `http://localhost:8080`
- **API 경로**: `/workers`
- **CORS**: 백엔드에서 프론트엔드 접근 허용

### 주요 API 엔드포인트
- `GET /workers` - 모든 작업자 조회
- `GET /workers/{id}` - 특정 작업자 조회
- `POST /workers` - 새로운 작업자 추가
- `PUT /workers/{id}` - 작업자 정보 수정
- `DELETE /workers/{id}` - 작업자 삭제

## 개발 환경

### 핫 리로드
- 파일 변경 시 자동으로 브라우저 새로고침
- Vite의 빠른 HMR(Hot Module Replacement) 지원

### 포트 충돌 방지
- `strictPort: true` 설정으로 포트 5173이 사용 중이면 에러 발생
- 다른 포트 사용 시 백엔드 CORS 설정도 수정 필요

### 브라우저 자동 열기
- 개발 서버 시작 시 자동으로 브라우저 열림
- `open: true` 설정

## 배포

### 정적 파일 생성
```bash
npm run build
```

### 웹 서버 설정
- `dist/` 폴더의 정적 파일을 웹 서버에 배포
- Nginx, Apache, 또는 CDN 사용

## 문제 해결

### 포트 5173이 사용 중인 경우
```bash
# 포트 사용 프로세스 확인
lsof -i :5173

# 프로세스 종료
kill -9 <PID>
```

### CORS 오류
- 백엔드가 `http://localhost:5173`에서의 접근을 허용하는지 확인
- `back/cctv/src/main/java/com/autoever/config/WebConfig.java` 확인

### 백엔드 연결 실패
- 백엔드가 `http://localhost:8080`에서 실행 중인지 확인
- `mvn spring-boot:run` 명령으로 백엔드 실행

## 개발 팁

1. **동시 실행**: 백엔드와 프론트엔드를 별도 터미널에서 실행
2. **API 테스트**: `ApiTestView.vue`에서 API 연결 상태 확인
3. **상태 관리**: Pinia를 사용한 전역 상태 관리
4. **라우팅**: Vue Router를 사용한 SPA 구현
