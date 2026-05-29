# Engineering Information System

해양플랜트 Equipment 관련 Engineering 정보를 통합 관리하기 위한 로컬 실행형 시스템.

- Frontend: React + TypeScript (Vite)
- Backend: FastAPI + Python
- 데이터 소스: 엑셀 파일 (별도 DB 미사용)
- 도면 뷰어: 브라우저 내장 PDF 뷰어 (PDF Viewer 우선)
- 실행 환경: 개인 PC 로컬 실행 기준

## 1. 폴더 구조

```
EngineeringDT_2/
├── backend/                          # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py                   # 앱 엔트리포인트
│   │   ├── config/                   # 환경설정 (.env 로드)
│   │   ├── models/                   # Pydantic 도메인 모델
│   │   ├── repositories/             # 엑셀 로더 + 데이터 접근
│   │   ├── services/                 # 비즈니스 로직
│   │   ├── api/routes/               # FastAPI 라우터
│   │   └── utils/                    # 공용 유틸
│   ├── requirements.txt
│   └── .env.example
├── frontend/                         # React + TS 프론트엔드
│   ├── src/
│   │   ├── api/                      # 백엔드 호출 모듈
│   │   ├── types/                    # 타입 정의
│   │   ├── pages/                    # 페이지 단위 컴포넌트
│   │   ├── components/               # 재사용 컴포넌트
│   │   ├── hooks/                    # 커스텀 훅
│   │   └── utils/                    # 공용 유틸
│   ├── package.json
│   ├── vite.config.ts
│   └── .env.example
├── Document_Storage/                 # 도면(PDF) 폴더
├── Tag_Register.xlsx
├── Document_List.xlsx
├── Document_to_Tag.xlsx
├── Manufacture_list.xlsx
├── PRD.txt
└── README.md
```

각 모듈은 단일 책임을 가지도록 분리되어 있어, 수정 시 해당 파일만 교체할 수 있다.

## 2. 사전 준비

- Python 3.11 이상
- Node.js 18 이상
- 엑셀 데이터 파일 4개 (`Tag_Register.xlsx`, `Document_List.xlsx`, `Document_to_Tag.xlsx`, `Manufacture_list.xlsx`)
- 도면 PDF 가 들어 있는 `Document_Storage` 폴더

## 3. 백엔드 실행

```powershell
# 1) 가상환경 활성화 (이미 venv502 가 존재한다면 그걸 사용)
.\venv502\Scripts\Activate.ps1

# 2) 의존성 설치
pip install -r backend\requirements.txt

# 3) .env 생성 (예시 파일 복사 후 경로 수정)
copy backend\.env.example backend\.env

# 4) FastAPI 실행 (backend 폴더에서)
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- 실행 후 `http://127.0.0.1:8000/api/health` 로 헬스체크 확인
- Swagger 문서: `http://127.0.0.1:8000/docs`

## 4. 프론트엔드 실행

```powershell
cd frontend
copy .env.example .env

npm install
npm run dev
```

- 기본 포트: `http://localhost:5173`
- 빌드: `npm run build`
- 린트: `npm run lint`
- 테스트: `npm run test`

## 5. 환경설정 파일

### backend/.env

| 변수명 | 설명 |
| --- | --- |
| `TAG_REGISTER_PATH` | Tag_Register.xlsx 절대경로 |
| `DOCUMENT_LIST_PATH` | Document_List.xlsx 절대경로 |
| `DOCUMENT_TO_TAG_PATH` | Document_to_Tag.xlsx 절대경로 |
| `MANUFACTURE_LIST_PATH` | Manufacture_list.xlsx 절대경로 |
| `DRAWING_STORAGE_PATH` | 도면(PDF) 저장 폴더 경로 |

### frontend/.env

| 변수명 | 설명 |
| --- | --- |
| `VITE_API_BASE_URL` | FastAPI 베이스 URL (기본 `http://localhost:8000`) |

## 6. 현재 진행 상태

본 단계에서는 폴더 구조와 빈 모듈, 기본 실행 구조만 구성되어 있다.
도메인 로직(Tag/Document/Hierarchy/Search/Manufacture)은 다음 단계에서 구현한다.
