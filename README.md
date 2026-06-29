# Plant Information System

해양플랜트 Equipment 관련 Engineering 정보를 통합 관리하기 위한 로컬 실행형 시스템.

- Frontend: React + TypeScript (Vite)
- Backend: FastAPI + Python
- 데이터 소스: 엑셀 파일 (별도 DB 미사용)
- 도면 뷰어: 브라우저 내장 PDF 뷰어 (PDF Viewer 우선)
- 실행 환경: 개인 PC 로컬 실행 기준

## 1. 폴더 구조

```
Plant_Information_System/
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

> **설정 검증:** 백엔드 의존성 설치 후, 서버를 띄우기 전에 저장소 루트에서
> `python verify_setup.py` 를 실행하면 Python 버전·의존성·데이터 경로·엑셀 로딩을
> 한 번에 점검하고 문제 항목과 해결법을 출력한다. 모두 통과하면 실행 준비 완료.

## 3. 백엔드 실행

```powershell
# 1) 가상환경 생성 및 활성화 (이미 venv 폴더가 있으면 그걸 활성화)
#    Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
#    macOS / Linux
#    python3 -m venv venv && source venv/bin/activate

# 2) 의존성 설치
pip install -r backend\requirements.txt

# 3) .env 생성 (예시 파일 복사 후 경로를 본인 PC 기준으로 수정 — 5장 참고)
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

경로는 **저장소 루트 기준 상대경로**로 적는다. 엑셀 4개 파일과 `Document_Storage/`
폴더가 저장소 루트에 함께 있는 기본 배치라면, **PC 가 바뀌어도 수정 없이 그대로 동작한다.**
(상대경로는 backend 코드가 저장소 루트를 기준으로 자동 해석한다.)

설정 절차:

```bash
cp backend/.env.example backend/.env       # Windows: copy backend\.env.example backend\.env
```

기본 `.env` 내용 (그대로 사용하면 됨):

```dotenv
TAG_REGISTER_PATH=Tag_Register.xlsx
DOCUMENT_LIST_PATH=Document_List.xlsx
DOCUMENT_TO_TAG_PATH=Document_to_Tag.xlsx
MANUFACTURE_LIST_PATH=Manufacture_list.xlsx
DRAWING_STORAGE_PATH=Document_Storage
```

> 참고: 데이터 파일을 **저장소 밖** 다른 위치(예: 공유 드라이브)에 둘 때만
> 해당 변수를 절대경로(`D:/data/Tag_Register.xlsx` 등)로 바꾼다. 절대경로를 적으면
> 그 값이 그대로 사용된다.
> `.env` 자체를 생략해도 위와 동일한 기본값(저장소 루트의 파일)이 적용된다.

| 변수명 | 설명 |
| --- | --- |
| `TAG_REGISTER_PATH` | Tag_Register.xlsx 경로 (상대=저장소 루트 기준) |
| `DOCUMENT_LIST_PATH` | Document_List.xlsx 경로 |
| `DOCUMENT_TO_TAG_PATH` | Document_to_Tag.xlsx 경로 |
| `MANUFACTURE_LIST_PATH` | Manufacture_list.xlsx 경로 |
| `DRAWING_STORAGE_PATH` | 도면(PDF) 저장 폴더 경로 |

경로가 맞는지 빠르게 확인하려면 `backend` 폴더에서 `python _smoke_test.py` 실행 시
각 엑셀의 행 수가 출력되면 정상이다.

### frontend/.env

| 변수명 | 설명 |
| --- | --- |
| `VITE_API_BASE_URL` | FastAPI 베이스 URL. **기본값은 비워둔다(빈 문자열).** 비워두면 모든 요청이 same-origin 으로 나가 Vite proxy 를 거쳐 백엔드로 전달되며, cross-origin 을 차단하는 사내 보안정책 환경에서도 도면 PDF 가 정상 표시된다. 별도 절대 URL 이 필요한 환경에서만 지정한다. |

## 6. 자주 겪는 문제

- **데이터가 안 나오고 `503` 오류** → 엑셀 파일이 저장소 루트에 없거나 파일명이 다른 경우.
  `python _smoke_test.py` 로 어떤 파일을 못 찾는지 확인한다. 데이터를 다른 위치에 두었다면
  5장처럼 해당 변수만 절대경로로 지정한다.
- **도면 PDF 가 안 보임** → `frontend/.env` 의 `VITE_API_BASE_URL` 을 비워두었는지 확인한다.
- **회사(폐쇄망) PC 의 Fasoo DRM** → 엑셀/PDF 읽기는 Fasoo DRM 해제를 자동 처리한다(Windows 전용).
  개발용 macOS/Linux 에서는 자동으로 무시(no-op)되어 동일하게 동작한다.
