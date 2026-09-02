<div align="center">

# 📁 A024 — File Upload & Serve Static Files (Images / PDFs)

### *Accept a file. Save it to disk. Serve it back over HTTP.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![python-multipart](https://img.shields.io/badge/python--multipart-0.0.12-blue?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-50_min-blueviolet?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **`POST /upload` accepts a `multipart/form-data` file via `UploadFile = File(...)`, streams it to `./uploads/`, and the `StaticFiles` mount at `/files/<filename>` serves it back as raw bytes.**

If you remember *"**U-S-M** — **U**pload, **S**ave, **M**ount"*, the rest of this README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: The Post Office](#-the-story-the-post-office)
- [🎯 What You Will Learn (10 Skills)](#-what-you-will-learn-10-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line (Heavily Commented)](#-anatomy-of-mainpy--line-by-line-heavily-commented)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧠 The Mental Model: How File Upload Works](#-the-mental-model-how-file-upload-works)
- [🆕 Every New Keyword Explained](#-every-new-keyword-explained)
- [🆚 multipart/form-data vs application/json](#-multipartform-data-vs-applicationjson)
- [🧪 Try It With curl](#-try-it-with-curl)
- [🔧 Variations](#-variations)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🎯 Interview Q&A](#-interview-qa)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: The Post Office 📮

Imagine a tiny post office with three desks:

| Desk | Job | HTTP |
|:-----|:----|:-----|
| 🪟 **Receiving window** | Accepts a parcel, writes your name on it, puts it on the shelf | `POST /upload` |
| 🗄️ **The shelf** | Holds every parcel, addressed by name | `./uploads/` directory |
| 🚪 **Pickup window** | "Give me parcel `photo.png`" — you can grab it yourself from the public shelf too | `GET /files/photo.png` (via `StaticFiles` mount) |

> 🧠 **Mnemonic:** "**U-S-M** — **U**pload (window) → **S**ave (shelf) → **M**ount (pickup).**"

---

## 🎯 What You Will Learn (10 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 📥 **`UploadFile`** | "The file object" |
| 2 | 📤 **`File(...)`** | "Marks the form field" |
| 3 | 📨 **`multipart/form-data`** | "The body type for files" |
| 4 | 💾 **`shutil.copyfileobj()`** | "Stream to disk" |
| 5 | 🗂️ **`os.path.join`** | "Build paths portably" |
| 6 | 📁 **`StaticFiles` mount** | "Serve a directory over HTTP" |
| 7 | 🛡️ **Path-traversal prevention** | "`os.path.basename` strips paths" |
| 8 | ✅ **Extension whitelist** | "Don't trust the user" |
| 9 | 🔁 **Streaming vs buffering** | "Don't load big files into memory" |
| 10 | 🪟 **`os.makedirs(..., exist_ok=True)`** | "Idempotent folder creation" |

---

## 📂 Project Structure

```
📁 A024_File_Upload_Serve_Static_Files_(Images_PDFs)/
├── 🐍 main.py              ← 95 lines: upload + static + metadata
├── 📦 requirements.txt     ← fastapi[standard] + python-multipart
├── 📂 uploads/             ← created on first run; files live here
└── 📖 README.md            ← you are here
```

> 🧠 The `uploads/` folder is auto-created. Files appear as `uploads/photo.png` and are reachable at `/files/photo.png`.

---

## ⚙️ Installation & Setup

```powershell
cd "D:\AllProgram\LEARN\Python\FastAPI\A024_File_Upload_Serve_Static_Files_(Images_PDFs)"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

> ⚠️ **`python-multipart` is required** for `File(...)` / `UploadFile` to work. `fastapi[standard]` includes it, but it's listed here explicitly for clarity.

---

## 🧬 Anatomy of `main.py` — Line by Line (Heavily Commented)

The new `main.py` is fully annotated. Key sections:

```python
# Whitelist of allowed file extensions. Prevents users from uploading
# arbitrary executables (e.g. .exe, .sh) and serving them back.
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".txt"}


def _safe_filename(filename: str) -> str:
    """
    Strip any path components from the filename.
    Prevents a malicious client from uploading "../../etc/passwd"
    by using `os.path.basename` to keep only the leaf name.
    """
    return os.path.basename(filename)


def _is_allowed(filename: str) -> bool:
    """True iff the file extension is in the whitelist."""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS
```

| Section | Code | 🧠 Why it's there |
|:--------|:-----|:------------------|
| Imports | `UploadFile`, `File`, `HTTPException` | The file-upload helpers |
| Imports | `StaticFiles` | Serve a directory over HTTP |
| Imports | `os`, `shutil` | Filesystem + streaming copy |
| Setup | `UPLOAD_DIR = "uploads"` | Where files are saved |
| Setup | `os.makedirs(..., exist_ok=True)` | Idempotent folder creation |
| Setup | `ALLOWED_EXTENSIONS` | Whitelist of safe extensions |
| Helpers | `_safe_filename()` | `os.path.basename` strips paths |
| Helpers | `_is_allowed()` | Extension whitelist check |
| Mount | `app.mount("/files", StaticFiles(...))` | Expose the directory over HTTP |
| POST `/upload` | `file: UploadFile = File(...)` | Required file form field |
| POST `/upload` | `_safe_filename` then `_is_allowed` | Security gates |
| POST `/upload` | `shutil.copyfileobj(file.file, buffer)` | Stream to disk |
| POST `/upload` | Return `{message, fileName, file_url}` | Friendly envelope |
| GET `/files-info/...` | Existence check | 404 if missing |

> ⚠️ **Route change vs. the original `main.py`:** the JSON "get file" route is now `/files-info/<filename>`, not `/files/<filename>`. The `/files/<filename>` URL is owned by the `StaticFiles` mount and returns the **raw file bytes**. Use `/files-info/<filename>` to get a JSON confirmation.

### The Three Magic Pieces

```python
app.mount("/files", StaticFiles(directory="uploads"), name="files")  # serve
file: UploadFile = File(...)                                          # receive
shutil.copyfileobj(file.file, buffer)                                 # save
```

> 🧠 **Mnemonic:** "**`mount` to serve, `File()` to receive, `copyfileobj` to save.**"

### 🎯 If you remember ONE thing
> **`UploadFile = File(...)` accepts the file; `shutil.copyfileobj` saves it; `StaticFiles` serves it. Whitelist extensions; strip paths.**

---

## 🛣️ API Endpoints

| Method | Endpoint | Body | Returns |
|:------:|:---------|:-----|:--------|
| 🟡 POST | `/upload` | `multipart/form-data` field `file` | `{message, fileName, file_url}` or 400/422 |
| 🟢 GET | `/files/<filename>` | — | **Raw file bytes** (via `StaticFiles`) |
| 🟢 GET | `/files-info/<filename>` | — | `{file_url}` or 404 |
| 🟢 GET | `/` | — | `{message: "file upload api running"}` |

---

## 🧠 The Mental Model: How File Upload Works

```mermaid
sequenceDiagram
    participant C as Client
    participant F as FastAPI
    participant D as ./uploads/
    participant S as StaticFiles

    Note over C,F: 1. UPLOAD (multipart/form-data)
    C->>F: POST /upload   body: multipart/form-data; file=@photo.png
    F->>F: UploadFile = File(...)  binds the file
    F->>F: _safe_filename + _is_allowed
    F->>D: open("uploads/photo.png", "wb") + shutil.copyfileobj(...)
    D-->>F: bytes flushed
    F-->>C: {message, fileName: "photo.png", file_url: "/files/photo.png"}

    Note over C,F: 2. SERVE (raw bytes)
    C->>F: GET /files/photo.png
    F->>S: StaticFiles routes the request
    S->>D: open("uploads/photo.png", "rb")
    D-->>S: bytes
    S-->>C: 200 OK   Content-Type: image/png
```

> 🧠 **The same file is reachable two ways:** `/files/photo.png` returns raw bytes (the static mount), and `/files-info/photo.png` returns a JSON envelope with the URL.

---

## 🆕 Every New Keyword Explained

### 1. `UploadFile` — the file object

**What:** A FastAPI class that wraps the uploaded file. Exposes:

- `file.filename` — original name from the client
- `file.content_type` — MIME type (e.g. `image/png`)
- `file.file` — a SpooledTemporaryFile (read like a normal Python file)
- `await file.read()` — read all bytes (async)
- `await file.close()` — close the underlying file

```python
file: UploadFile = File(...)
print(file.filename)        # "photo.png"
print(file.content_type)    # "image/png"
```

> 🧠 **Mnemonic:** "**`UploadFile` = a SpooledTemporaryFile with metadata.**"

### 2. `File(...)` — the form-field marker

**What:** Tells FastAPI to bind this parameter to a **`multipart/form-data`** field. `...` means required; `File()` (no value) means optional.

```python
file: UploadFile = File(...)             # required
file: UploadFile | None = File(None)     # optional
```

> 🧠 **Mnemonic:** "**`File(...)` = 'this param comes from the form body'**."

### 3. `multipart/form-data` — the body type

**What:** An HTTP body format for sending **binary data** (files) + text fields in one request. Each part is delimited by a boundary string. The browser sets this automatically when you submit `<form enctype="multipart/form-data">`.

```
POST /upload HTTP/1.1
Content-Type: multipart/form-data; boundary=----abc

------abc
Content-Disposition: form-data; name="file"; filename="photo.png"
Content-Type: image/png

<binary bytes>
------abc--
```

> 🧠 **Mnemonic:** "**Files = multipart. JSON = no files.**"

### 4. `shutil.copyfileobj(src, dst)` — stream copy

**What:** Copies bytes from `src` to `dst` in chunks. Doesn't load the whole file into memory. Use it to save an upload to disk.

```python
with open("out.png", "wb") as f:
    shutil.copyfileobj(file.file, f)
```

> 🧠 **Mnemonic:** "**Stream chunks, don't load all.**"

### 5. `os.path.join(*parts)` — build a path

**What:** Joins path parts with the OS separator (`/` on Linux/macOS, `\` on Windows). Safer than string concatenation.

```python
os.path.join("uploads", "photo.png")    # 'uploads/photo.png' or 'uploads\\photo.png'
```

> 🧠 **Mnemonic:** "**Use `join`, not `+`.**"

### 6. `os.path.basename(path)` — keep only the filename

**What:** Strips the directory portion. The single most important security helper for file uploads — without it, `filename = "../../etc/passwd"` would write outside `uploads/`.

```python
os.path.basename("../../etc/passwd")    # "passwd"
os.path.basename("photo.png")           # "photo.png"
```

> 🧠 **Mnemonic:** "**`basename` = 'no slashes, no escapes'**."

### 7. `os.path.splitext(name)` — split extension

**What:** Returns `(root, ext)`, e.g. `("photo", ".png")`. Use the extension to whitelist file types.

```python
os.path.splitext("photo.PNG")    # ('photo', '.PNG')  ← still uppercase
os.path.splitext("photo.png")[1].lower()    # '.png'
```

> 🧠 **Mnemonic:** "**`splitext` = `(root, .ext)`.**"

### 8. `os.makedirs(path, exist_ok=True)` — idempotent folder creation

**What:** Creates the folder (and parents) if missing; does NOT raise if it already exists. Use it once at startup.

```python
os.makedirs("uploads", exist_ok=True)    # safe to call repeatedly
```

> 🧠 **Mnemonic:** "**`exist_ok=True` = 'no error if it's already there'**."

### 9. `StaticFiles(directory=...)` — serve a directory

**What:** A FastAPI class that serves every file in `directory` under the mount path. Perfect for read-only public assets.

```python
app.mount("/files", StaticFiles(directory="uploads"), name="files")
# GET /files/photo.png  →  uploads/photo.png
```

| Pros | Cons |
|:-----|:-----|
| Zero code for serving | No auth, no rate limit |
| Correct `Content-Type` headers | No access control |
| Streaming, no memory buffer | No on-the-fly transforms |

> 🧠 **Mnemonic:** "**`StaticFiles` = a public read-only folder over HTTP.**"

### 10. `app.mount(path, app, name=...)` — sub-application

**What:** Attaches another ASGI app (like `StaticFiles`) at a URL prefix. Requests to `/files/...` are routed to the `StaticFiles` app instead of your routes.

```python
app.mount("/files", StaticFiles(directory="uploads"), name="files")
```

> 🧠 **Mnemonic:** "**`mount` = 'forward this URL prefix to a sub-app'**."

---

## 🆚 multipart/form-data vs application/json

| Aspect | `application/json` | `multipart/form-data` |
|:-------|:-------------------|:----------------------|
| Body type | Single JSON text blob | Multiple parts, each with its own headers + bytes |
| Files? | ❌ (base64 only) | ✅ native binary |
| Use case | API CRUD with JSON payloads | File uploads, mixed form fields |
| Browser sets it when... | You use `fetch(..., {headers: {"Content-Type": "application/json"}})` | You submit `<form enctype="multipart/form-data">` |
| `curl` flag | `-H "Content-Type: application/json" -d '{"...": ...}'` | `-F "file=@photo.png"` |

```bash
# JSON (no files)
curl -X POST http://.../api \
  -H "Content-Type: application/json" \
  -d '{"name": "adnan"}'

# multipart (with file)
curl -X POST http://.../upload \
  -F "file=@photo.png"
```

> 🧠 **Mnemonic:** "**JSON = no files. multipart = files.**"

---

## 🧪 Try It With curl

### 1. Make a tiny PNG to upload

```bash
# PowerShell — creates a 1x1 red PNG
[System.IO.File]::WriteAllBytes("red.png", [byte[]](137,80,78,71,13,10,26,10,0,0,0,13,73,72,68,82,0,0,0,1,0,0,0,1,8,2,0,0,0,144,119,83,222,0,0,0,12,73,68,65,84,8,153,99,248,255,255,63,0,5,254,2,254,220,204,89,231,0,0,0,0,73,69,78,68,174,66,96,130))
```

### 2. Upload it

```bash
curl -X POST http://127.0.0.1:8000/upload -F "file=@red.png"
```

```json
{
  "message": "File uploaded successfully",
  "fileName": "red.png",
  "file_url": "http://127.0.0.1:8000/files/red.png"
}
```

### 3. Fetch the raw file (StaticFiles mount)

```bash
curl -o red_downloaded.png http://127.0.0.1:8000/files/red.png
```

### 4. Get the JSON info

```bash
curl http://127.0.0.1:8000/files-info/red.png
```

```json
{"file_url":"http://127.0.0.1:8000/files/red.png"}
```

### 5. Reject a `.exe` (extension whitelist)

```bash
curl -X POST http://127.0.0.1:8000/upload -F "file=@evil.exe"
```

```http
HTTP/1.1 400 Bad Request
{"detail":"File type not allowed. Allowed: ['.gif', '.jpeg', '.jpg', '.pdf', '.png', '.txt', '.webp']"}
```

### 6. Reject a path-traversal attempt

```bash
curl -X POST http://127.0.0.1:8000/upload -F "file=@photo.png;filename=../../etc/passwd"
```

The server receives `filename = "../../etc/passwd"`. After `os.path.basename`, it becomes `"passwd"`, which fails the extension whitelist (`.passwd` not in the list) → 400.

---

## 🔧 Variations

### Variation 1: Multiple files at once

```python
from typing import List

@app.post("/upload-many")
def upload_many(files: List[UploadFile] = File(...)):
    saved = []
    for file in files:
        filename = _safe_filename(file.filename or "")
        if not _is_allowed(filename):
            continue
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved.append(filename)
    return {"saved": saved}
```

```bash
curl -X POST http://127.0.0.1:8000/upload-many \
  -F "files=@a.png" -F "files=@b.png" -F "files=@c.pdf"
```

### Variation 2: Rename uploads to a UUID

```python
import uuid

@app.post("/upload-uuid")
def upload_uuid(file: UploadFile = File(...)):
    ext = os.path.splitext(_safe_filename(file.filename or ""))[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Bad extension")
    new_name = f"{uuid.uuid4().hex}{ext}"
    with open(os.path.join(UPLOAD_DIR, new_name), "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"fileName": new_name, "file_url": f"http://127.0.0.1:8000/files/{new_name}"}
```

### Variation 3: Stream the upload directly (no temp file)

```python
from fastapi.responses import StreamingResponse

@app.post("/upload-and-process")
async def upload_and_process(file: UploadFile = File(...)):
    # Process the upload as a stream (e.g. compute a hash, scan, etc.)
    hash_obj = __import__("hashlib").sha256()
    while chunk := await file.read(1024 * 1024):    # 1 MB chunks
        hash_obj.update(chunk)
    return {"sha256": hash_obj.hexdigest(), "filename": file.filename}
```

### Variation 4: Add a size limit

```python
from starlette.middleware.base import BaseHTTPMiddleware

class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app, max_bytes: int):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request, call_next):
        cl = request.headers.get("content-length")
        if cl and int(cl) > self.max_bytes:
            raise HTTPException(413, f"File too big (>{self.max_bytes} bytes)")
        return await call_next(request)

app.add_middleware(LimitUploadSize, max_bytes=10 * 1024 * 1024)    # 10 MB
```

### Variation 5: Delete a file

```python
@app.delete("/files/{filename}")
def delete_file(filename: str):
    filename = _safe_filename(filename)
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(404, "Not found")
    os.remove(path)
    return {"deleted": filename}
```

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| 422 "field required" | Sent JSON instead of multipart | Use `-F "file=@..."` in curl, or `<form enctype="multipart/form-data">` in HTML |
| `ImportError: python-multipart` | `File(...)` requires the multipart parser | `pip install python-multipart` |
| File written outside `uploads/` | Used `filename` as-is, no `os.path.basename` | Always `_safe_filename` first |
| `.exe` uploaded and served back | No extension whitelist | Reject anything not in `ALLOWED_EXTENSIONS` |
| `FileNotFoundError` in startup | `UPLOAD_DIR` didn't exist | `os.makedirs(..., exist_ok=True)` at startup |
| Big upload eats all RAM | Read whole file into memory | Use `shutil.copyfileobj` (streaming) |
| Same filename overwrites silently | No collision check | Rename with UUID, or check `os.path.exists` first |
| Wrong `Content-Type` returned | StaticFiles auto-detects; some browsers confused | Set explicit `media_type` if you proxy manually |
| 500 on missing file at `/files/...` | StaticFiles returns 404 itself | That's correct — the JSON endpoint is for the envelope, not the file |

### The "JSON body" Trap

```bash
# ❌ Wrong — sends JSON, server expects multipart
curl -X POST http://127.0.0.1:8000/upload \
  -H "Content-Type: application/json" \
  -d '{"file": "..."}'

# ✅ Right — sends multipart with `-F`
curl -X POST http://127.0.0.1:8000/upload \
  -F "file=@photo.png"
```

### The "Path Traversal" Trap

```python
# ❌ Vulnerable — user controls the destination path
file_path = os.path.join(UPLOAD_DIR, file.filename)
# if file.filename == "../../etc/passwd", this writes outside uploads/

# ✅ Safe — strip path components
filename = os.path.basename(file.filename or "")
file_path = os.path.join(UPLOAD_DIR, filename)
```

### The "python-multipart Missing" Trap

```
# ❌ Without python-multipart:
422 Unprocessable Entity
{"detail":[{"loc":["body","file"],"msg":"field required","type":"value_error.missing"}]}

# ✅ Install it
pip install python-multipart
```

> 🧠 **Mnemonic:** "**Files = `python-multipart`. `os.path.basename` = no escapes.**"

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| 3-step flow | **U-S-M** | Upload, Save, Mount |
| `UploadFile` | **Spooled temp file** | Has `.file`, `.filename`, `.content_type` |
| `File(...)` | **Form-field marker** | Required / optional |
| `multipart/form-data` | **Files = multipart** | JSON = no files |
| `shutil.copyfileobj` | **Stream chunks** | Don't load all |
| `os.path.basename` | **No slashes, no escapes** | Strips path components |
| `os.path.splitext` | **(root, .ext)** | Whitelist by extension |
| `os.makedirs(exist_ok=True)` | **Idempotent** | Safe to call repeatedly |
| `StaticFiles(directory=...)` | **Public read-only folder** | Mount at `/files` |
| `app.mount(...)` | **Sub-app at a prefix** | Forwards to `StaticFiles` |
| Whitelist | **Don't trust the user** | Extension check before save |

---

## 🧪 Recall Test

1. What does `File(...)` mark a parameter as?
2. What's the body type for file uploads?
3. How do you stream an upload to disk without loading it all into memory?
4. How do you prevent path-traversal?
5. How do you whitelist file types?
6. How do you serve a directory over HTTP?
7. Why is `python-multipart` required?
8. What's the difference between `/files/<filename>` and `/files-info/<filename>`?

> 8/8 → file upload is yours.

---

## 🎯 Interview Q&A

### Q1: How do you accept a file upload in FastAPI?

**Answer:** Use `UploadFile = File(...)` and declare the parameter as `multipart/form-data`:

```python
from fastapi import UploadFile, File

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    contents = file.file.read()
    ...
```

`File(...)` makes the field required; `File()` makes it optional.

> **One-liner:** *"`UploadFile = File(...)` for a required form file."*

### Q2: How do you save the upload to disk?

**Answer:** Open a file in `"wb"` mode and use `shutil.copyfileobj` to stream the bytes:

```python
import shutil

with open("uploads/photo.png", "wb") as f:
    shutil.copyfileobj(file.file, f)
```

This streams in chunks; it never loads the whole file into memory.

> **One-liner:** *"`shutil.copyfileobj` to stream to disk."*

### Q3: How do you serve a directory over HTTP?

**Answer:** Mount `StaticFiles` on a URL prefix:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/files", StaticFiles(directory="uploads"), name="files")
```

Now `GET /files/photo.png` returns the contents of `uploads/photo.png` with the right `Content-Type`.

> **One-liner:** *"`app.mount('/files', StaticFiles(...))` to serve a folder."*

### Q4: How do you prevent path-traversal attacks?

**Answer:** Always run the filename through `os.path.basename` first. This strips any directory components, so `../../etc/passwd` becomes just `passwd`.

```python
import os

filename = os.path.basename(file.filename or "")
file_path = os.path.join(UPLOAD_DIR, filename)
```

> **One-liner:** *"`os.path.basename` strips path components."*

### Q5: How do you whitelist file types?

**Answer:** Check the extension against an allowed set, ideally with a leading `.` and lower-cased:

```python
ALLOWED = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".txt"}

def _is_allowed(name: str) -> bool:
    return os.path.splitext(name)[1].lower() in ALLOWED
```

> **One-liner:** *"Whitelist extensions; never trust the user."*

### Q6: Why is `python-multipart` required for file uploads?

**Answer:** `File(...)` and `UploadFile` use the **multipart/form-data** body format, which Python's stdlib doesn't parse. `python-multipart` is the parser FastAPI uses under the hood. Without it, the request body is opaque and the form fields can't be read.

> **One-liner:** *"`python-multipart` parses the multipart body."*

### Q7: What's the difference between buffering and streaming an upload?

**Answer:**

| Buffering | Streaming |
|:----------|:----------|
| `contents = await file.read()` then `f.write(contents)` | `shutil.copyfileobj(file.file, f)` |
| Whole file in memory | Chunked, constant memory |
| Fine for small files | Required for big files (videos, PDFs) |

> **One-liner:** *"Big files = stream. Small files = buffer is fine."*

### Q8: How do you let users download the file they uploaded?

**Answer:** Three options:

1. **`StaticFiles` mount** — easiest, but no auth/rate-limit
2. **`FileResponse`** — read the file and stream it back with custom headers
3. **`StreamingResponse`** — for on-the-fly generation (e.g. zip on demand)

```python
from fastapi.responses import FileResponse

@app.get("/download/{filename}")
def download(filename: str):
    return FileResponse(os.path.join(UPLOAD_DIR, _safe_filename(filename)),
                        filename=filename)    # ← triggers "Save As"
```

> **One-liner:** *"Public download = `StaticFiles`. Authenticated download = `FileResponse`."*

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A023](../A023_OAuth2_JWT_Authentication_Secure_Routes_Password_Hashing/) |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A025 (planned) — File upload to S3 / cloud storage |
| ➡️ Future | A026 (planned) — Authenticated downloads + signed URLs |

---

<div align="center">

### 📁 *Receive it, save it, serve it.* 📁

Made with ❤️, `UploadFile = File(...)`, and `shutil.copyfileobj`.

</div>