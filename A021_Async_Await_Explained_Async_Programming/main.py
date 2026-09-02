# =========================================================
# A021 — Async / Await Explained (Async Programming)
# =========================================================
# Walks the difference between sync and async route handlers:
#   - GET /                       → async def + await asyncio.sleep(3)
#   - The endpoint DOES NOT block the event loop while waiting.
#   - Other requests can be served during the 3s wait.
# =========================================================

# --- Standard library: time for sync timing, asyncio for async sleep ---
import time
import asyncio

# --- FastAPI: the framework ---
from fastapi import FastAPI

# 1. Create the FastAPI app instance (Uvicorn serves THIS object)
app = FastAPI()


# =========================================================
# ASYNC ROUTE — GET /
# =========================================================
# `async def` makes this a *coroutine function*. When called, it returns a
# coroutine object that the event loop schedules and runs to completion.
# `await asyncio.sleep(3)` YIELDS control back to the event loop for 3s,
# letting other requests be served in the meantime.
@app.get("/")
async def home():
    # `asyncio.sleep(3)` is a NON-BLOCKING sleep. It tells the event loop
    # "wake me up in 3 seconds" and immediately returns control.
    # Compare to `time.sleep(3)` which would BLOCK the entire worker.
    await asyncio.sleep(3)

    return {
        "message": "Async API"
    }


# =========================================================
# Reference: what sync would look like
# =========================================================
# Sync functions block the worker thread for the full duration:
# def task():
#     time.sleep(3)    # ← BLOCKS the whole server for 3 seconds
#     return "Task done"
#
# Async functions yield control while waiting:
# async def task():
#     await asyncio.sleep(3)    # ← server handles other requests meanwhile
#     return "Done"
# =========================================================
