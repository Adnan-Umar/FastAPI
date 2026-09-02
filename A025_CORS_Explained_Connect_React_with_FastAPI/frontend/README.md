# A025 — React Frontend (CORS demo)

A minimal Vite + React 18 app that talks to the FastAPI server in this folder.

## Stack

- **Vite 5** — dev server + bundler
- **React 18** — UI
- **No build config beyond the default** — kept simple on purpose

## Quick start

```powershell
cd "D:\AllProgram\LEARN\Python\FastAPI\A025_CORS_Explained_Connect_React_with_FastAPI\frontend"
npm install
npm run dev
```

Vite will start on <http://localhost:5173> — exactly the origin that `main.py`'s
CORS allow-list trusts. The app has three buttons that hit the FastAPI server
on `http://127.0.0.1:8000`.

## What it does

| Button | Endpoint | Purpose |
|:-------|:---------|:--------|
| `GET /` | FastAPI | Verify the API is up |
| `GET /todos` | FastAPI | Load the sample todos |
| `POST /todos` | FastAPI | Send a new todo as JSON |

If CORS is misconfigured, the browser will show an error like
`No 'Access-Control-Allow-Origin' header is present`. The error message is
displayed at the bottom of the page.

## Files

- `src/main.jsx` — React entry point
- `src/App.jsx` — the demo UI
- `src/api.js` — `fetch` helpers for the three endpoints
- `src/index.css` — small dark-mode stylesheet
- `vite.config.js` — Vite config (port 5173, strict)
- `package.json` — React + Vite deps

## Troubleshooting

| Error | Cause | Fix |
|:------|:------|:----|
| `Network Error` in console | FastAPI not running | `cd .. && uvicorn main:app --reload` |
| `No 'Access-Control-Allow-Origin' header` | `localhost` ≠ `127.0.0.1` in the allow-list | Both are listed in `main.py` |
| `404` on `/todos` | Old server without the route | Restart `uvicorn` after editing `main.py` |
| `CORS policy: credentials` warning | `allow_credentials=True` without explicit origin | `allow_origins` is a literal list, not `*` — already correct here |
