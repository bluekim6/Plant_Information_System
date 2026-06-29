# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Plant Information System — a **locally-run** app for browsing engineering information about offshore-plant equipment (Tags, Documents/drawings, Manufacturers). There is **no database**: all reference data comes from four Excel files, and user-generated Comments/History are persisted to JSON files. Runs as two processes: FastAPI backend (`:8000`) + React/Vite frontend (`:5173`).

## Commands

**Backend** (run from `backend/`, a Python venv must be active — `../venv529/` exists on this machine):
```bash
pip install -r requirements.txt
cp .env.example .env          # then edit paths to ABSOLUTE local paths
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
python _smoke_test.py         # quick check that repositories read the Excel files
```
Health check: `http://127.0.0.1:8000/api/health` · Swagger: `http://127.0.0.1:8000/docs`

**Frontend** (run from `frontend/`):
```bash
npm install
npm run dev        # Vite dev server on :5173, proxies /api -> :8000
npm run build      # tsc -b && vite build
npm run lint
npm run test       # vitest (run once); single file: npm run test -- src/path/file.test.ts
```

There is **no backend test suite** — only `backend/_smoke_test.py`. Frontend tests use vitest but currently none are committed.

## Environment / data wiring (the most common source of breakage)

- Settings (`app/config/settings.py`) loads `.env` relative to the `backend/` dir (not cwd). Path values may be **relative or absolute**: a `field_validator` resolves any relative path against the **repo root** (`_REPO_ROOT = backend/..`), and absolute paths are used as-is. The four Excel paths + `DRAWING_STORAGE_PATH` also have repo-root defaults, so the app runs even with no `.env`. Missing/incorrect paths surface as `503` errors at request time, not startup crashes (preload only logs errors).
- The Excel files (`Tag_Register.xlsx`, `Document_List.xlsx`, `Document_to_Tag.xlsx`, `Manufacture_list.xlsx`) and `Document_Storage/` live in the **repo root**, so the default relative paths work on any machine. Only override with an absolute path when data lives outside the repo.
- `frontend/.env`: `VITE_API_BASE_URL` is intentionally **empty by default**, so all `/api/*` calls go same-origin and Vite's proxy forwards them to `:8000`. This is deliberate — a corporate security policy blocks cross-origin PDF embedding, so drawings must be served same-origin. Only set an absolute URL in environments that require it.

## Backend architecture

Layered, one responsibility per module. Request flow:

```
api/routes/*  ->  services/*  ->  repositories/*  ->  data/excel_loader.py  ->  Excel
                                                   ->  data/json_store.py    ->  JSON (comments/history)
```

- **`data/excel_loader.py`** — loads each Excel into a pandas DataFrame, **cached by file mtime** (per-file, thread-safe), auto-reloads when the file changes. Reads everything as `dtype=str`, fills NaN with `""`, strips whitespace. This is the live loader. NOTE: `repositories/excel_loader.py` also exists but is **dead code — not imported anywhere**; use `data/excel_loader.py`.
- **`core/column_map.py`** — single source of truth mapping code constants to **raw Excel column names**. If an Excel header changes, edit only this file. Tag attributes are *dynamic* columns identified by the `"Attribute "` prefix (Attribute A~BD), collected into a dict in `TagDetail`.
- **`repositories/*`** — convert DataFrames into Pydantic domain models (`models/schemas.py`). DataFrames never leak past this layer.
- **`services/*`** — business logic / joins across repositories (e.g. tag→documents).
- **Routes may call repositories directly** for simple read-only list endpoints (e.g. `routes/tags.py` calls `findAllTags`), and go through a service when there's logic. Both patterns are intentional.
- **Errors**: raise `ResourceNotFoundError` etc. from `core/exceptions.py`; `api/error_handlers.py` maps them to JSON `ErrorResponse` with proper status (404/503). Don't return raw HTTP errors from routes.
- **Drawings**: `services/drawing_service.py` maps `documentNo` → `Document_Storage/{documentNo}.pdf`; `routes/drawings.py` streams it via `FileResponse`.
- **Fasoo DRM** (`utils/decrypt_fasoo.py`): every Excel/PDF read passes through `decrypt_fasoo_file()` first. It's **Windows-only** (uses `f_nxldr.dll`) and a **no-op on macOS/Linux** (returns the original path), so it's transparent in local dev but required in the company's closed network. Don't remove these calls.

### Python style note
Functions and variables use **camelCase** (e.g. `getTagDetail`, `loadTagRegister`, `tagNo`) rather than PEP 8 snake_case. Match the surrounding style when editing.

## Frontend architecture

- **`api/client.ts`** — single shared axios instance (`baseURL` from `VITE_API_BASE_URL`, default `""`). All `api/*.ts` modules call through it.
- **`hooks/useAsyncResource.ts`** — generic fetch hook (data/loading/error, cancellation on input change, empty input → reset). Most data-loading hooks (`useSelectedTag`, `useTagDocuments`, etc.) wrap it. Prefer reusing it over hand-rolling `useEffect` fetches.
- **`pages/MainPage.tsx`** is the single page; it holds the master view state (`tag-info | tag-documents | document-detail`) plus selected tag/document/manufacture, and coordinates Header (search) + Sidebar (system tree) + the detail panels. New navigation generally means adding a `MainView` state branch here.
- PDFs are embedded same-origin (see env note above) so the browser's built-in PDF viewer renders them without cross-origin blocking.

## Reference

`PRD.txt`, `creat_code.md` (Fasoo DRM design), and `설명매뉴얼.txt` / `프로그래밍프롬프트.txt` contain product/spec context. `README.md` is partly stale (says modules are empty stubs and references a `venv502`/Windows-only flow — the modules are in fact implemented).
