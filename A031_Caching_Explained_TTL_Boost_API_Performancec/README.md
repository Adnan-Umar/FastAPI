<div align="center">

# ⏳ A031 — Caching Explained (TTL) + Boost API Performance

### *Scrape once. Serve from cache for 60 seconds. Measure the speedup.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![In-Memory](https://img.shields.io/badge/cache-in__memory-lightgrey?style=for-the-badge)
![TTL](https://img.shields.io/badge/TTL-60s-orange?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-50_min-blueviolet?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **Time-to-live (TTL) caching means: fetch data once, store it in a variable, and reuse it for N seconds. Check `time.time() - last_fetch > TTL`; if not expired, skip the expensive upstream call.**

If you remember *"`if time.time() - last_fetch > TTL: refetch else serve cache`"*, the rest of this README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: The Lunch Box](#-the-story-the-lunch-box)
- [🎯 What You Will Learn (10 Skills)](#-what-you-will-learn-10-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line (Heavily Commented)](#-anatomy-of-mainpy--line-by-line-heavily-commented)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧠 The Mental Model: TTL Cache Flow](#-the-mental-model-ttl-cache-flow)
- [🆕 Every New Keyword Explained](#-every-new-keyword-explained)
- [🆚 In-Memory vs Redis vs HTTP Cache](#-in-memory-vs-redis-vs-http-cache)
- [🆚 TTL vs LRU vs FIFO](#-ttl-vs-lru-vs-fifo)
- [🧪 Try It With curl](#-try-it-with-curl)
- [🔧 Variations](#-variations)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🎯 Interview Q&A](#-interview-qa)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: The Lunch Box 🍱

You're a student. Buying lunch costs **₹50** and takes **10 minutes**. Packing leftovers costs ₹0 and takes 5 seconds. So you:

1. **Day 1 — Buy.** You pay ₹50, bring back a big tiffin (the full data set).
2. **Days 1–6 — Reuse.** You reheat the same tiffin. Free and instant.
3. **Day 7 — Buy again.** The tiffin is "stale" (past its TTL). You buy fresh.

> 🧠 **Mnemonic:** "**Stale after TTL. Refetch = buy fresh. Cache = reheat.**"

---

## 🎯 What You Will Learn (10 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | ⏰ **`time.time()`** | "Epoch seconds, always moving" |
| 2 | 📐 **TTL comparison** | "`time.time() - last > TTL` = stale" |
| 3 | 📦 **In-memory cache variable** | "A module-level list/dict" |
| 4 | 🔁 **"Refetch if stale" pattern** | `if time.time() - last > TTL: refetch` |
| 5 | ⚡ **Cache vs fresh timing** | `time_taken` shows the difference |
| 6 | 🌐 **Why cache upstream APIs** | "Avoid slow / flaky / rate-limited upstreams" |
| 7 | 🗑️ **Cache invalidation** | "TTL is automatic expiry" |
| 8 | 🪤 **`global` keyword** | "Needed to reassign a module-level var" |
| 9 | 🏎️ **Cache hit = near 0s** | "Microsecond vs seconds" |
| 10 | 🔄 **Cache-aside pattern** | "App reads cache; writes cache" |

---

## 📂 Project Structure

```
📁 A031_Caching_Explained_TTL_Boost_API_Performancec/
├── 🐍 main.py              ← crawl HN + cache for 60s, return timing
├── 📦 requirements.txt     ← fastapi[standard] + requests + beautifulsoup4
└── 📖 README.md             ← you are here
```

> 🧠 The cache lives in two module-level variables (`cache_data`, `last_fetch`) — it resets when the server restarts. For multi-process or multi-server, see Redis (Variations).

---

## ⚙️ Installation & Setup

```powershell
cd "D:\AllProgram\LEARN\Python\FastAPI\A031_Caching_Explained_TTL_Boost_API_Performancec"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

> ⚠️ Crawls `https://news.ycombinator.com/` — needs network access.

---

## 🧬 Anatomy of `main.py` — Line by Line (Heavily Commented)

The full file is now annotated (code logic unchanged — only comments added, plus a named `CACHE_TTL_SECONDS = 60` constant replacing the magic `60`).

```python
# 1. Create the FastAPI app instance
app = FastAPI()

# =========================================================
# CACHE STORAGE
# =========================================================
cache_data = []
last_fetch = 0
CACHE_TTL_SECONDS = 60


@app.get("/news")
def get_news():
    global cache_data, last_fetch
    start = time.time()

    # 1. CACHE CHECK — is the cache still fresh?
    if time.time() - last_fetch > CACHE_TTL_SECONDS:
        print("Fetching fresh data")
        url = "https://news.ycombinator.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        cache_data = [
            item.text for item in soup.find_all("span", class_="titleline")
        ]
        last_fetch = time.time()
    else:
        print("Using Cache data")

    end = time.time()
    time_taken = round(end - start, 4)

    return {
        "time_taken": time_taken,
        "data": cache_data[:5]
    }
```

| Line | Code | 🧠 Why it's there |
|:----:|:-----|:------------------|
| 27–29 | `cache_data = []`, `last_fetch = 0` | The two cache vars |
| 31 | `CACHE_TTL_SECONDS = 60` | Named TTL constant (was magic 60) |
| 33 | `global cache_data, last_fetch` | Needed to reassign module vars |
| 41 | `time.time() - last_fetch > CACHE_TTL_SECONDS` | **Is the cache stale?** |
| 44 | `requests.get(url)` | Fetch upstream only if stale |
| 49–51 | `cache_data = [...]` | Overwrite cache with fresh data |
| 53 | `last_fetch = time.time()` | Stamp the cache |
| 63 | `return {"time_taken", "data"}` | Show cache vs fresh timing |

> 🧠 **The single decision line:** `if time.time() - last_fetch > TTL: refetch else serve cache`. Everything else supports it.

### 🎯 If you remember ONE thing
> **`if time.time() - last_fetch > TTL: refetch. Else: return the cache. The `time_taken` field shows the speedup.**

---

## 🛣️ API Endpoints

| Method | Endpoint | Returns |
|:------:|:---------|:--------|
| 🟢 GET | `/news` | `{time_taken: float, data: [title1..5]}` (cache hit ~0.0001s, miss ~2s) |

---

## 🧠 The Mental Model: TTL Cache Flow

```mermaid
flowchart TD
    A[GET /news] --> B{Is cache stale?}
    B -- "time.time() - last_fetch > 60" -->|Yes (stale or never fetched)| C[Fetch upstream]
    B -- "within 60s" -->|No (fresh)| D[Use cache]
    C --> E[requests.get HN]
    E --> F[BeautifulSoup parse]
    F --> G[cache_data = [...50 titles]]
    G --> H[last_fetch = time.time]
    H --> I[Return cache_data[:5]]
    D --> I
    I --> J[Response: {time_taken, data}]
```

> 🧠 **The first request fetches; the next 59 seconds are fast.**

---

## 🆕 Every New Keyword Explained

### 1. TTL — Time to Live

**What:** The maximum age (in seconds) a cached value is considered valid. After TTL expires, the cache is stale and must be refreshed.

```python
CACHE_TTL_SECONDS = 60
if time.time() - last_fetch > CACHE_TTL_SECONDS:
    refetch()
```

> 🧠 **Mnemonic:** "**TTL = 'how long may this stale?'**"

### 2. `time.time()` — epoch seconds

**What:** Returns the current Unix timestamp (float seconds since 1970). **Never** use `datetime.now()` for cache TTL — it's timezone-naive and can jump with DST.

```python
now = time.time()           # 1725000000.123
age = now - last_fetch      # 60.5 → stale
```

> 🧠 **Mnemonic:** "**`time.time()` = epoch. `datetime.now()` = local clock (avoid).**"

### 3. Cache hit vs cache miss

**What:** A cache **hit** means the data was found in the cache (fast). A cache **miss** means it wasn't (must be fetched, slow).

| `time.time() - last_fetch > TTL` | Result | Time |
|:---------------------------------|:-------|:-----|
| `True` | miss → fetch | slow (seconds) |
| `False` | hit → return cache | fast (microseconds) |

> 🧠 **Mnemonic:** "**Miss = fetch. Hit = instant.**"

### 4. In-memory cache (module-level variable)

**What:** A plain Python variable (`cache_data = []`, a dict, or a class attribute) that persists across requests **in the same process**. Resets on restart.

```python
cache_data = []    # module-level — shared by all requests
```

| Pros | Cons |
|:-----|:-----|
| Zero deps, simple | One cache per process |
| Fast (same process) | Wiped on restart |
| Good for single process | Not shared across replicas |

> 🧠 **Mnemonic:** "**In-memory = one process's RAM.**"

### 5. `global` keyword

**What:** Lets a function assign to a **module-level** variable instead of a local.

```python
cache_data = []
def update():
    global cache_data
    cache_data = [...]    # rebinds the module var
```

> 🧠 **Mnemonic:** "**`global` = 'I mean THE module variable, not a local'**."**"

### 6. Cache-aside pattern

**What:** The application logic explicitly reads the cache, and on a miss, fetches from the source and writes back. (Contrast: write-through, write-behind.)

```python
if stale:
    data = fetch_upstream()
    cache_data = data
    last_fetch = time.time()
return cache_data
```

> 🧠 **Mnemonic:** "**Cache-aside = 'app reads, app writes'**."

### 7. Cache invalidation

**What:** The moment a cached value becomes stale. With TTL, invalidation is **automatic**: the next request after the TTL expires is a miss and refetches. (Hard invalidation — explicit `cache.clear()` — is the other kind.)

> 🧠 **Mnemonic:** "**TTL invalidation = automatic staleness.**"

### 8. Cache stampede

**What:** A pathological case where many concurrent requests all miss the cache at once (e.g. on startup) and all hammer the upstream simultaneously. Mitigations: lock + single fetch, or background refresh.

> 🧠 **Mnemonic:** "**Many misses at once = stampede.**"

### 9. Stale-while-revalidate

**What:** A strategy where: on cache hit, you serve the **stale** data immediately, then **asynchronously** refresh in the background. Users never wait for the upstream.

> 🧠 **Mnemonic:** "**Serve stale now, refresh in the background.**"

### 10. `time_taken` as a cache indicator

**What:** By measuring how long a request took (including or excluding the upstream fetch), you can see whether it was a cache hit or miss.

```python
start = time.time()
# ... cache check + maybe fetch ...
time_taken = round(time.time() - start, 4)
return {"time_taken": time_taken, "data": ...}
```

| Cache | `time_taken` |
|:------|:-------------|
| hit | ~0.0001 |
| miss | ~2 (upstream fetch + parse) |

> 🧠 **Mnemonic:** "**Tiny time = cache hit.**"

---

## 🆚 In-Memory vs Redis vs HTTP Cache

| Cache type | Where | Pros | Cons |
|:-----------|:------|:-----|:-----|
| **In-memory** (this module) | Process RAM | Zero deps, fast | One per process; wipes on restart |
| **Redis** | External server | Shared across instances; TTL built-in; pub/sub invalidation | Needs an extra service |
| **HTTP cache** (browser/CDN) | Client-side | Reduces load to your server | You control server response, not always the client |
| **functools.lru_cache** | In-process | Automatic key handling | Sync-only; no TTL by default |

> 🧠 **Mnemonic:** "**In-memory = simple. Redis = shared. LRU_cache = auto-keys.**"

---

## 🆚 TTL vs LRU vs FIFO

| Strategy | Evicts by | Good for |
|:---------|:----------|:---------|
| **TTL** (this module) | Age (stale after N seconds) | Data that changes periodically (news, rates) |
| **LRU** (Least Recently Used) | Access recency (evicts oldest-accessed) | Hot datasets (keep popular items) |
| **FIFO** (First In, First Out) | Insert order | Simple queues; rarely optimal |

> 🧠 **Mnemonic:** "**TTL = age. LRU = usage. FIFO = order.**"

---

## 🧪 Try It With curl

### 1. First call (cache MISS — fetches from HN)

```bash
curl http://127.0.0.1:8000/news
```

```json
{
  "time_taken": 2.4567,
  "data": ["T1: Some Hacker News Title", "T2: ...", "T3: ...", "T4: ...", "T5: ..."]
}
```

### 2. Second call within 60 seconds (cache HIT — instant)

```bash
curl http://127.0.0.1:8000/news
```

```json
{
  "time_taken": 0.0003,
  "data": ["T1: ...", "T2: ...", "T3: ...", "T4: ...", "T5: ..."]
}
```

The data is the same but `time_taken` dropped from ~2s to ~0.0003s.

### 3. Wait 60+ seconds, call again (cache MISS again)

```bash
sleep 61    # (PowerShell: Start-Sleep -Seconds 61)
curl http://127.0.0.1:8000/news
# time_taken jumps back to ~2s; data refreshed
```

### 4. Watch the server logs

```
INFO:     Uvicorn running on http://127.0.0.1:8000
Using Cache data       ← you'll see this on hits
Fetching fresh data     ← you'll see this on misses
```

---

## 🔧 Variations

### Variation 1: Redis cache with built-in TTL

```python
# pip install redis
import redis, json
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

@app.get("/news")
def get_news():
    cached = r.get("hn_titles")
    if cached:
        print("Cache hit (Redis)")
        titles = json.loads(cached)
    else:
        response = requests.get("https://news.ycombinator.com/", timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        titles = [item.text for item in soup.find_all("span", class_="titleline")]
        r.setex("hn_titles", 60, json.dumps(titles))    # 60s TTL
    return {"time_taken": 0, "data": titles[:5]}
```

> 🧠 Redis handles TTL + eviction automatically; no `last_fetch` variable needed.

### Variation 2: `functools.lru_cache` with TTL

```python
from functools import lru_cache
import time

@lru_cache(maxsize=1)
def _fetch_hn():
    response = requests.get("https://news.ycombinator.com/", timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    return [item.text for item in soup.find_all("span", class_="titleline")]

@lru_cache(maxsize=1)
def _fetch_time():
    return time.time()

def _stale():
    return time.time() - _fetch_time() > 60

@app.get("/news")
def get_news():
    if _stale():
        _fetch_hn.cache_clear()
        _fetch_time.cache_clear()
    titles = _fetch_hn()
    return {"time_taken": round(time.time() - _fetch_time(), 4), "data": titles[:5]}
```

> 🧠 **Mnemonic:** "`lru_cache` caches by args; for TTL, clear on staleness."

### Variation 3: Stale-while-revalidate (never block the client)

```python
import asyncio

@app.get("/news")
async def get_news():
    if time.time() - last_fetch > CACHE_TTL_SECONDS:
        if not is_refreshing:    # single-flight
            is_refreshing = True
            asyncio.create_task(_refresh_in_background())
        # serve stale data NOW; refresh happens async
    return {"time_taken": ..., "data": cache_data[:5]}

async def _refresh_in_background():
    try:
        cache_data[:] = [item.text for item in soup.find_all("span", class_="titleline")]
        global last_fetch
        last_fetch = time.time()
    finally:
        is_refreshing = False
```

### Variation 4: `cachetools.TTLCache`

```python
# pip install cachetools
from cachetools import TTLCache

cache = TTLCache(maxsize=1, ttl=60)

def get_cached_titles():
    if "titles" not in cache:
        response = requests.get("https://news.ycombinator.com/", timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        cache["titles"] = [item.text for item in soup.find_all("span", class_="titleline")]
    return cache["titles"]
```

### Variation 5: Thread-safe in-memory cache

```python
import threading

_cache_lock = threading.Lock()

@app.get("/news")
def get_news():
    global cache_data, last_fetch
    with _cache_lock:
        if time.time() - last_fetch > CACHE_TTL_SECONDS:
            # ... fetch ...
            cache_data = [...]
            last_fetch = time.time()
    return {"data": cache_data[:5]}
```

> 🧠 **Important:** In-memory caches are **not thread-safe** by default. Use a `Lock` if multiple threads write to the same variable.

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| Cache never expires | Compared `last_fetch` instead of `time.time() - last_fetch` | `time.time() - last_fetch > TTL` |
| All requests re-fetch (cache always stale) | `last_fetch` reset every request, or TTL is 0 | Make sure `last_fetch = time.time()` is INSIDE the stale branch |
| `global` not declared | Local assignment to `cache_data` instead of reassigning module var | Add `global cache_data, last_fetch` |
| Race condition | Multiple requests all think cache is stale | Use a lock, or background refresh |
| `time.time()` jumps with system clock | DST change, NTP sync | `time.time()` is epoch; for monotonic, use `time.monotonic()` |
| Cache wiped on restart | In-memory | Persist to disk, or use Redis |
| `time_taken` is 0 on a hit | `start`/`end` both read the clock | That's correct — hit is fast (microseconds) |

### The "Cache never expires" Trap

```python
# ❌ This is WRONG — last_fetch is read, never compared
if last_fetch > TTL:     # ← compares timestamp (big number) to 60
    refetch()

# ✅ Correct
if time.time() - last_fetch > TTL:
    refetch()
```

### The "global not declared" Trap

```python
# ❌ Python creates a NEW local `cache_data` and shadows the module var
cache_data = []
def get_news():
    cache_data = fetch()    # ← local! module var unchanged
    return cache_data

# ✅ Declare global
def get_news():
    global cache_data
    cache_data = fetch()    # ← module var is updated
    return cache_data
```

> 🧠 **Mnemonic:** "**If you `cache_data = ...` inside the function, you MUST `global` it.**"

### The "No timeout on requests" Trap

```python
# ❌ If HN hangs, your worker hangs too
response = requests.get(url)

# ✅ Cache mitigates this, but still timeout the upstream
response = requests.get(url, timeout=10)
```

> 🧠 **Even with caching, the first fetch still needs a timeout.**

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| Cache TTL | **Age check** | `time.time() - last > TTL` |
| Cache hit | **Instant** | ~0.0001s |
| Cache miss | **Fetch** | ~2s |
| `global` | **Module var** | Needed to reassign |
| TTL expiry | **Stale after N** | Auto-refresh on next request |
| Redis | **Shared + TTL built-in** | Multi-process |
| LRU | **Oldest usage evicted** | Hot keys stay |
| FIFO | **Oldest inserted evicted** | Simple queue |
| Stampede | **Too many misses** | Lock + background refresh |
| Stale-revalidate | **Serve stale, refresh async** | User never waits |

---

## 🧪 Recall Test

1. What's the TTL comparison line?
2. What do `cache_data` and `last_fetch` store?
3. What's the difference between a cache hit and a miss?
4. Why do you need `global cache_data, last_fetch`?
5. What happens on the *first* request?
6. How does the `time_taken` field reveal cache hits?
7. What's one problem with in-memory caching?
8. What's a cache stampede and how do you mitigate it?

> 8/8 → caching is yours.

---

## 🎯 Interview Q&A

### Q1: What is TTL-based caching?

**Answer:** A cache where each entry expires after a fixed number of seconds ("time-to-live"). On a cache miss (entry absent or expired), you fetch fresh data; on a hit, you return the cached value.

```python
TTL = 60
if time.time() - last_fetch > TTL:
    cache_data = fetch_upstream()
    last_fetch = time.time()
return cache_data
```

> **One-liner:** *"Cache for N seconds, then refetch."*

### Q2: How do you check if a cache is stale?

**Answer:** Compare the elapsed time since the last fetch against the TTL.

```python
if time.time() - last_fetch > TTL:
    # cache is stale
```

> **One-liner:** *"`time.time() - last_fetch > TTL` = stale.**"*

### Q3: Why cache upstream API calls?

**Answer:**

1. **Speed** — return cached data in microseconds instead of seconds
2. **Reliability** — serve cached data if the upstream is down/slow
3. **Rate limits** — don't hit the upstream's rate limit
4. **Cost** — upstream API calls may be billed per request

> **One-liner:** *"Faster, more reliable, avoids rate limits and costs."*

### Q4: What is a cache stampede?

**Answer:** A thundering herd problem: a cache entry expires at time T, and N concurrent requests all miss and all rush to refetch at once, overwhelming the upstream. Mitigations:

1. **Single-flight / lock** — only one request fetches; others wait
2. **Stale-while-revalidate** — serve stale data, refresh in the background
3. **Jittered TTL** — randomize expiry so not everything expires at once

> **One-liner:** *"Many concurrent misses = stampede. Lock or background-refresh."*

### Q5: What's the cache-aside pattern?

**Answer:** The application **explicitly** checks the cache and decides to fetch or return. The cache and the data source are separate.

```python
def get():                                   # cache-aside
    data = cache.get(key)                    # 1. check cache
    if not data:
        data = fetch_from_source()          # 2. fetch if miss
        cache.set(key, data, ttl=60)        # 3. write back
    return data                             # 4. return
```

> **One-liner:** *"App checks cache, fetches on miss, writes back. Explicit."*

### Q6: What's the difference between in-memory cache and Redis cache?

**Answer:**

| In-memory | Redis |
|:----------|:------|
| One per process | Shared across all processes/servers |
| Wipes on restart | Persists, survives restarts |
| Zero config | Needs a server |
| Fast (same process) | Fast (network hop) |
| Not shared by replicas | Shared by replicas |

> **One-liner:** *"In-memory = one process. Redis = all processes."*

### Q7: Should you cache everything?

**Answer:** No. Cache data that is: (a) **read often**, (b) **expensive to compute/fetch**, and (c) **stale-tolerant** (a few minutes of staleness is acceptable). Don't cache per-user, per-request data with huge variance — you'll waste memory.

> **One-liner:** *"Cache: hot + expensive + stale-tolerant. Not everything."*

### Q8: How do you avoid a cache stampede in a simple FastAPI app?

**Answer:** Two practical approaches:

1. **Stale-while-revalidate** — serve stale data immediately, start a background task to refresh. Client never waits.
2. **Single-flight with a lock** — only one request refetches; concurrent requests wait for its result.

```python
import threading
_refresh_lock = threading.Lock()

if stale():
    with _refresh_lock:
        if stale():     # double-check inside the lock
            cache_data = fetch_upstream()
            last_fetch = time.time()
```

> **One-liner:** *"Double-checked locking: lock, re-check, then refresh once."*

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A030](../A030_Pagination_Explained_Limit_Real_API_Example/) |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A032 (planned) — Production caching: Redis + distributed locks + cache invalidation |
| ➡️ Future | A033 (planned) — Background refresh with `asyncio` + `asyncio.Lock` |

---

<div align="center">

### ⏳ *Fetch once. Serve fast. Refetch when stale.* ⏳

Made with ❤️, `cache_data = [...]`, and `if time.time() - last_fetch > TTL:`.

</div>