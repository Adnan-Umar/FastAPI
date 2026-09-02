# =========================================================
# A024 — File Upload + Serve Static Files (Images / PDFs)
# =========================================================
# Endpoints:
#   - POST /upload              → accept a multipart file, save to ./uploads,
#                                 return its public URL under /files/<filename>
#   - GET  /files/<filename>    → return the file's public URL (or 404)
#   - GET  /files/<filename>    → ALSO served by the StaticFiles mount,
#                                 so the same URL returns the raw bytes
#   - GET  /                    → health check
# =========================================================

# --- FastAPI: framework + UploadFile / File helpers + HTTP errors ---
from fastapi import FastAPI, UploadFile, File, HTTPException

# --- StaticFiles: serve files from a directory over HTTP ---
from fastapi.staticfiles import StaticFiles

# --- stdlib: filesystem + high-level file copy ---
import os
import shutil

# 1. Create the FastAPI app instance (Uvicorn serves THIS object)
app = FastAPI()


# =========================================================
# STEP 1 — Ensure the upload directory exists
# =========================================================
# Files are saved to ./uploads (relative to the working directory).
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)    # idempotent; no error if it exists

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


# =========================================================
# STEP 2 — Mount a static-files directory at /files
# =========================================================
# Now any file inside ./uploads is reachable at /files/<filename>.
# Example:  ./uploads/photo.png  →  http://127.0.0.1:8000/files/photo.png
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")


# =========================================================
# STEP 3 — Upload endpoint
# =========================================================
# Accepts `multipart/form-data` (the default for HTML file inputs and
# for `curl -F "file=@photo.png"`). The `File(...)` makes the field
# required; omitting the file returns a 422.
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    # 1. Sanitize the filename: strip any path components
    filename = _safe_filename(file.filename or "")
    if not filename:
        raise HTTPException(status_code=400, detail="File not selected")

    # 2. Reject disallowed extensions
    if not _is_allowed(filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {sorted(ALLOWED_EXTENSIONS)}"
        )

    # 3. Stream the upload to disk in chunks (no large in-memory buffer)
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)    # efficient streaming copy

    # 4. Return a friendly envelope with the public URL
    return {
        "message": "File uploaded successfully",
        "fileName": filename,
        "file_url": f"http://127.0.0.1:8000/files/{filename}"
    }


# =========================================================
# STEP 4 — Get-file-metadata endpoint
# =========================================================
# NOTE: the StaticFiles mount at /files already returns the raw bytes for
# any existing file. This JSON endpoint just confirms existence and
# returns the public URL.
@app.get("/files-info/{filename}")
def get_file_info(filename: str):
    filename = _safe_filename(filename)
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return {
        "file_url": f"http://127.0.0.1:8000/files/{filename}"
    }


# =========================================================
# STEP 5 — Health check
# =========================================================
@app.get("/")
def home():
    return {
        "message": "file upload api running"
    }
