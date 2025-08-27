# 📝 프로젝트 협업 컨벤션

본 문서는 원활한 협업과 코드 품질 유지를 위한 규칙을 정의합니다. 모든 팀원은 아래 규칙을 숙지하고 준수해야 합니다.

---

## 🌍 공통 협업 규칙

기술 스택과 관계없이 모든 프로젝트 구성원이 따라야 하는 공통 규칙입니다.

### 1. Git 브랜치 전략

**GitHub Flow**를 기본 전략으로 사용합니다.

* **`main`**: 항상 배포 가능한 상태를 유지하는 프로덕션 브랜치입니다. 직접적인 push는 금지되며, 오직 `develop` 브랜치의 Pull Request를 통해서만 병합됩니다.

* **`develop`**: 다음 릴리즈를 준비하는 개발 브랜치입니다. 기능 개발이 완료되면 이 브랜치로 Pull Request를 보냅니다.

* **`feature/{기능-이름}`**: 새로운 기능 개발을 위한 브랜치입니다. `develop` 브랜치에서 생성하며, 기능 이름은 영어 소문자와 하이픈(-)을 사용합니다. (예: `feature/face-recognition-auth`)

### 2. 커밋 메시지 규칙

**Conventional Commits** 명세를 따릅니다. 이는 커밋 히스토리의 가독성을 높이고, 변경 로그 생성을 자동화하는 데 도움이 됩니다.

* **제목(subject)은 반드시 영어로 작성합니다.**

* **형식:** `<type>(<scope>): <subject>`

  * `<scope>`는 변경된 부분의 범위를 나타내며, **작성할 필요가 없는 경우 생략 가능**합니다.

* **예시:**

  * `feat: Add face recognition login`

  * `feat(auth): Add JWT authentication`

  * `fix(log): Fix date format error in access log`

  * `docs: Update API documentation for user registration`

  * `refactor(user): Remove duplicate code in UserService`

  * `test(auth): Add test cases for face recognition success/failure`

### 3. API 명세 관리

**OpenAPI 3.0 (Swagger)**를 사용하여 API를 설계하고 문서화합니다.

* **Spring Boot**: `springdoc-openapi` 라이브러리를 사용하여 코드 기반으로 API 문서를 자동 생성합니다.

* 프론트엔드와 AI 서버는 이 문서를 기준으로 API를 호출하고 개발합니다.

### 4. 코드 리뷰

모든 코드는 `develop` 브랜치에 병합되기 전 **Pull Request(PR)**를 통해 **최소 1명 이상의 동료에게 코드 리뷰**를 받아야 합니다.

* PR 제목과 설명은 다른 사람이 이해하기 쉽게 상세히 작성합니다.

* 리뷰어는 코드의 로직, 스타일, 잠재적 버그 등을 꼼꼼히 확인하고 건설적인 피드백을 제공합니다.

---

## 🧪 테스트 작성 가이드라인 (Testing Guidelines)

코드의 안정성과 품질을 보장하기 위해 테스트 코드 작성을 의무화합니다.

* **원칙**:

  * 새로운 기능을 추가할 경우, 해당 기능에 대한 테스트 코드를 반드시 함께 작성합니다.

  * 버그를 수정할 경우, 해당 버그가 재현되는 테스트 케이스를 먼저 작성하고 버그를 수정한 후 테스트가 통과하는 것을 확인합니다.

* **Spring Boot**:

  * **단위 테스트 (Unit Test)**: `JUnit 5`와 `Mockito`를 사용합니다. **Service 계층**의 비즈니스 로직은 반드시 단위 테스트로 검증해야 합니다.

  * **통합 테스트 (Integration Test)**: `@SpringBootTest`를 사용하여 **Controller 계층**의 API End-point가 의도대로 동작하는지 검증합니다.

* **Vue.js**:

  * **단위 테스트 (Unit Test)**: `Vitest` 또는 `Jest`를 사용합니다. 컴포넌트의 props, event, slot과 **Pinia Store**의 action, getter 로직을 테스트합니다.

* **Flask**:

  * **단위 테스트 (Unit Test)**: `Pytest`를 사용합니다. AI 모델의 핵심 로직(특징 추출, 유사도 비교 등)은 Mock 데이터를 사용하여 반드시 단위 테스트로 검증합니다.

---

## 🐛 이슈 및 버그 리포팅 (Issue & Bug Reporting)

GitHub 이슈를 통해 모든 작업을 추적하고 관리합니다. 명확한 소통을 위해 아래 템플릿을 사용해주세요.

### 기능 제안 (Feature Request)

```markdown
**Is your feature request related to a problem? Please describe.**
(이 기능이 어떤 문제를 해결하기 위해 필요한지 명확하고 간결하게 설명해주세요.)

**Describe the solution you'd like**
(어떤 해결책을 원하는지 구체적으로 설명해주세요.)

**Additional context**
(추가적인 정보나 스크린샷이 있다면 여기에 추가해주세요.)
```

### 버그 리포트 (Bug Report)

```markdown
**Describe the bug**
(버그에 대한 명확하고 간결한 설명을 작성해주세요.)

**To Reproduce**
(버그를 재현하기 위한 단계를 순서대로 작성해주세요.)
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
(원래 기대했던 동작은 무엇인지 설명해주세요.)

**Screenshots**
(가능하다면, 문제를 이해하는 데 도움이 되는 스크린샷을 첨부해주세요.)

**Environment (please complete the following information):**
 - OS: [e.g. iOS]
 - Browser [e.g. chrome, safari]
 - Version [e.g. 22]
```

---

## ☕️ Spring Boot (Java) 컨벤션

* **네이밍 & 스타일**: [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)를 따릅니다.

* **패키지 구조**: 도메인 중심의 계층형 구조를 사용합니다.

  ```
  com.project.
  ├── domain/
  │   ├── user/
  │   │   ├── UserController.java
  │   │   ├── UserService.java
  │   │   ├── UserRepository.java
  │   │   └── dto/
  │   │       └── UserResponse.java
  ```

* **DTO 사용**: Controller에서는 반드시 DTO(Data Transfer Object)를 사용하여 데이터를 주고받습니다. Service 계층에서 Entity와 DTO 간의 변환을 책임집니다.

* **린터 & 포맷터 상세 설정**:

  * **Linter**: **SonarLint**를 IDE에 설치하여 실시간으로 코드 품질을 검사합니다.
    * **설치 방법 (IntelliJ 기준)**:
      1. `File` > `Settings` > `Plugins` 로 이동합니다.
      2. `Marketplace` 탭에서 `SonarLint`를 검색하여 설치 후 IDE를 재시작합니다.
    * **사용법**:
      - 설치 후 별도 설정 없이 코드를 작성하면 SonarLint가 잠재적 버그나 코드 스멜을 실시간으로 하이라이트 해줍니다.
      - 문제 패널에서 제안하는 수정 가이드를 따라 코드를 개선합니다.

  * **Formatter**: IntelliJ의 기본 포맷터를 사용하며, 팀 공통의 `formatter.xml` 설정 파일을 공유하여 코드 스타일을 통일합니다.
    * **설정 파일 공유**:
      - **내보내기(Export)**: 팀 리더가 `File` > `Settings` > `Editor` > `Code Style`에서 `Export` > `IntelliJ IDEA code style XML`을 선택하여 `formatter.xml` 파일을 생성하고 Git 저장소에 공유합니다.
      - **가져오기(Import)**: 팀원은 공유된 `formatter.xml` 파일을 다운로드 받은 후, 같은 메뉴에서 `Import Scheme`을 통해 적용합니다.
    * **사용법**:
      - 코드 작성 후 단축키 `Ctrl + Alt + L` (Windows/Linux) 또는 `Cmd + Option + L` (Mac)을 눌러 파일 전체를 포맷팅합니다.

---

## 🎨 Vue.js (JavaScript/TypeScript) 컨벤션

* **스타일 가이드**: [Vue 공식 스타일 가이드 (필수)](https://ko.vuejs.org/style-guide/) 규칙을 최우선으로 따릅니다.

* **상태 관리**: 전역 상태 관리가 필요할 경우 **Pinia**를 사용합니다.

* **린터 & 포맷터**:

  * **Linter**: **ESLint** (`eslint-plugin-vue` 포함)를 사용하여 코드의 잠재적 오류를 방지합니다.

  * **Formatter**: **Prettier**를 사용하여 일관된 코드 스타일을 유지합니다.

* **자동화**: **Husky**와 **lint-staged**를 사용하여, `git commit` 시점에 자동으로 ESLint 검사와 Prettier 포맷팅이 실행되도록 강제합니다.

---

## 🤖 Flask (Python) 컨벤션

* **스타일 가이드**: [PEP 8](http://peps.python.org/pep-0008/) 스타일 가이드를 반드시 준수합니다.

* **의존성 관리**: **Poetry**를 사용하여 패키지 의존성을 관리하고 가상 환경을 통일합니다.

* **린터 & 포맷터**:

  * **Formatter**: **Black**을 사용하여 코드 스타일을 강제 통일합니다.

  * **Linter**: **Flake8**을 사용하여 PEP 8 위반 및 잠재적 오류를 검사합니다.

  * **타입 체크**: **Mypy**를 도입하여 정적 타입 검사를 수행하고 코드의 안정성을 높입니다.

* **자동화**: **pre-commit** 훅을 설정하여 커밋 시점에 Black, Flake8, Mypy가 자동으로 실행되도록 합니다.
