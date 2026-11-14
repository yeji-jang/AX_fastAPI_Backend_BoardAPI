<div align="center">

# 📋 FastAPI Board

**FastAPI와 레이어드 아키텍처로 만든 게시판 백엔드 API**

회원 · JWT 인증 · 게시판 · 게시글 · 댓글

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy_2-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat-square&logo=uv&logoColor=white)

</div>

---

## ✨ 주요 기능

| 구분 | 기능 |
|---|---|
| 👤 **회원** | 회원가입(이메일 중복 확인), 비밀번호 변경, 소프트 삭제 |
| 🔐 **인증** | JWT(HS512) 액세스 토큰 발급, 로그아웃 시 토큰 블랙리스트 처리 |
| 🗂️ **게시판** | 게시판 생성 · 조회 · 설정 변경 · 삭제 (관리자 전용), 게시판별 권한 설정 |
| 📝 **게시글** | 작성 · 상세 · 수정 · 삭제, 검색과 페이징 |
| 💬 **댓글** | 작성 · 목록 · 수정 · 삭제 |
| 🙋 **비회원** | 이름과 비밀번호로 글 · 댓글 작성, 비밀번호로 수정 · 삭제 (bcrypt 해싱) |

### 게시글 검색

`search_type`으로 어디에서 검색할지 고를 수 있어요.

| 값 | 검색 대상 |
|---|---|
| `ALL` | 제목 + 내용 + 작성자명 + 작성자 이메일 |
| `TITLE` | 제목 |
| `CONTENT` | 내용 |
| `TITLE_CONTENT` | 제목 + 내용 |
| `AUTHOR_NAME` | 작성자명 |
| `AUTHOR_EMAIL` | 작성자 이메일 |

### 권한 규칙

- **게시판 권한**: 게시판마다 목록 · 조회 · 작성 · 댓글 목록 · 댓글 작성 권한을 `ALL` / `USER` / `ADMIN` 중에서 따로 정해요.
- **수정 · 삭제 권한**: 관리자 → 회원 본인 → 비회원 비밀번호 순서로 확인해요.

---

## 🏗️ 아키텍처

도메인별(`user`, `auth`, `board`)로 모듈을 나누고, 각 모듈 안을 4개 계층으로 구성했어요.

```mermaid
flowchart TB
    P["🌐 Presentation<br/>Router · Schema · Depends 플레이스홀더"]
    A["⚙️ Application<br/>Service (유스케이스)"]
    D["💎 Domain<br/>Entity · Value Object · Repository 인터페이스"]
    I["🗄️ Infrastructure<br/>SQLAlchemy Model · Mapper · Repository 구현"]
    W["🔌 Wiring<br/>dependency_overrides로 구현체 주입"]

    P --> A --> D
    I -. 구현 .-> D
    W -. 주입 .-> P
```

- **Domain**은 다른 계층에 의존하지 않아요. 비즈니스 규칙과 검증은 모두 엔티티 안에 있어요.
- **Presentation**은 `provide_*` 같은 플레이스홀더 의존성만 알고 있어요.
- **Wiring**이 앱 시작 시 FastAPI `dependency_overrides`로 실제 구현을 연결해요. 그래서 테스트할 때 구현체를 쉽게 바꿔 끼울 수 있어요.

<details>
<summary><b>📁 폴더 구조 펼치기</b></summary>

```
src/
├── main.py                  # 앱 진입점 (lifespan, 예외 핸들러, 라우터 등록)
├── wiring/                  # 모듈별 의존성 주입 설정
│   ├── user.py
│   ├── auth.py
│   └── board.py
├── shared/core/             # 공통 모듈
│   ├── database.py          #   비동기 DB 엔진 / 세션
│   ├── exceptions.py        #   HTTP 예외 계층
│   ├── exception_handlers.py
│   ├── logger.py
│   ├── models.py            #   Base, 생성/수정/삭제 시각 컬럼
│   └── schemas.py           #   공통 응답 포맷 APIResponse
├── user/                    # 회원
├── auth/                    # 인증
└── board/                   # 게시판 · 게시글 · 댓글
    ├── domain/              #   엔티티, 값 객체, 리포지토리 인터페이스
    ├── application/         #   서비스
    ├── infrastructure/      #   SQLAlchemy 모델 · 매퍼 · 리포지토리, bcrypt
    └── presentation/        #   라우터, 스키마, 의존성
```

</details>

---

## 🚀 시작하기

### 1. 준비물

- [Python 3.13](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/)
- [Docker](https://www.docker.com/) (PostgreSQL 실행용)

### 2. 저장소 받기 & 패키지 설치

```bash
git clone https://github.com/yeji-jang/fastAPI-Backend---Board.git
cd fastAPI-Backend---Board
uv sync
```

### 3. PostgreSQL 실행

```bash
docker run -d --name board-db -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:17
```

> 💡 5432 포트를 이미 쓰고 있다면 `-p 5433:5432`처럼 다른 포트를 쓰고, `.env`의 `DATABASE_URL` 포트도 같이 바꿔주세요.

### 4. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 만들어요.

```env
# DB
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
SQL_ECHO=False
CONNECTION_POOL_SIZE=10
CONNECTION_POOL_MAX_SIZE=20

# Logger
LOGGING_MODE=info
LOGGER_NAME=app

# JWT (HS512 → 64바이트 이상 권장)
JWT_SECRET_KEY="여기에-64자-이상의-랜덤-문자열"
```

> ⚠️ `JWT_SECRET_KEY`가 없으면 서버가 시작되지 않아요. 아래 명령으로 만들 수 있어요.
> ```bash
> python -c "import secrets; print(secrets.token_urlsafe(64))"
> ```

### 5. 서버 실행

```bash
uv run uvicorn main:app --reload --app-dir src
```

서버가 시작되면 테이블이 자동으로 만들어져요.

| 문서 | 주소 |
|---|---|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

### 6. 관리자 계정 만들기

관리자를 만드는 API는 따로 없어요. 회원가입을 한 뒤 DB에서 역할을 바꿔주세요.

```bash
docker exec -it board-db psql -U postgres -c "UPDATE users SET role='ADMIN' WHERE email='admin@test.com';"
```

---

## 📡 API 목록

> 🔒 = 로그인 필요 · 👑 = 관리자 전용 · 그 밖의 API는 게시판 권한 설정을 따라요.

### 👤 회원 `/v1/users`

| Method | Endpoint | 설명 |
|:---:|---|---|
| `POST` | `/v1/users` | 회원가입 |
| `PATCH` | `/v1/users/{user_id}/password` | 🔒 비밀번호 변경 |

### 🔐 인증 `/v1/auth`

| Method | Endpoint | 설명 |
|:---:|---|---|
| `POST` | `/v1/auth/login` | 로그인 (액세스 토큰 발급) |
| `POST` | `/v1/auth/logout` | 🔒 로그아웃 (토큰 무효화) |

### 🗂️ 게시판

| Method | Endpoint | 설명 |
|:---:|---|---|
| `POST` | `/v1/boards` | 👑 게시판 생성 |
| `GET` | `/v1/boards` | 게시판 목록 |
| `GET` | `/v1/boards/{board_id}` | 게시판 조회 |
| `PUT` | `/v1/boards/{board_id}` | 👑 게시판 설정 변경 |
| `DELETE` | `/v1/boards/{board_id}` | 👑 게시판 삭제 |

### 📝 게시글

| Method | Endpoint | 설명 |
|:---:|---|---|
| `POST` | `/v1/boards/{board_id}/posts` | 게시글 작성 |
| `GET` | `/v1/boards/{board_id}/posts` | 게시글 목록 (검색 · 페이징) |
| `GET` | `/v1/posts/{post_id}` | 게시글 상세 |
| `PUT` | `/v1/posts/{post_id}` | 게시글 수정 |
| `DELETE` | `/v1/posts/{post_id}` | 게시글 삭제 |

### 💬 댓글

| Method | Endpoint | 설명 |
|:---:|---|---|
| `POST` | `/v1/posts/{post_id}/comments` | 댓글 작성 |
| `GET` | `/v1/posts/{post_id}/comments` | 댓글 목록 |
| `PUT` | `/v1/comments/{comment_id}` | 댓글 수정 |
| `DELETE` | `/v1/comments/{comment_id}` | 댓글 삭제 |

---

## 📦 공통 응답 형식

모든 API는 같은 형식으로 응답해요.

<table>
<tr><th>✅ 성공</th><th>❌ 실패</th></tr>
<tr>
<td>

```json
{
  "success": true,
  "code": "OK",
  "message": "요청이 성공적으로 처리되었습니다.",
  "errors": null,
  "data": { "...": "..." },
  "responded_at": "2026-11-15T12:00:00Z"
}
```

</td>
<td>

```json
{
  "success": false,
  "code": "VALIDATION_ERROR",
  "message": "비밀번호 제약 조건을 만족하지 못했습니다.",
  "errors": {
    "password": ["비밀번호는 8자 이상이어야 하며 ..."]
  },
  "data": null,
  "responded_at": "2026-11-15T12:00:00Z"
}
```

</td>
</tr>
</table>

---

## 📏 입력 규칙

| 항목 | 규칙 |
|---|---|
| 회원 비밀번호 | 8자 이상, 영문 · 숫자 · 특수문자 포함 |
| 회원 이름 | 2~20자 |
| 게시판 ID | 영문 소문자로 시작, 영문 소문자 · 숫자 · `_` · `-` 2~30자 (예: `freetalk`, `qna`) |
| 비회원 이름 | 20자 이하 |
| 비회원 비밀번호 | 6자 이상 |
| 게시글 목록 `page_size` | 최대 100 |
