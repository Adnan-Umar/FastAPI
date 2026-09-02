<div align="center">

# 📄 A030 — Pagination Explained (Limit) + Real API Example

### *Paginate a live-crawled news list with `page` and `limit` query parameters.*

<br/>

![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![requests](https://img.shields.io/badge/requests-2.32.3-252525?style=for-the-badge)
![BeautifulSoup](https://img.shields.io/badge/beautifulsoup4-4.12.3-252525?style=for-the-badge)
![Pagination](https://img.shields.io/badge/offset--limit-orange?style=for-the-badge)
![Difficulty](https://img.shields.io/badge/Level-Intermediate-orange?style=for-the-badge)
![Reading Time](https://img.shields.io/badge/Read_Time-50_min-blueviolet?style=for-the-badge)

</div>

---

## 🧠 The One-Sentence Summary

> **Pagination = return a slice of results at a time instead of the whole list. Offset-limit pagination uses `(page-1) * limit` as the start index and `page * limit` as the end.**

If you remember *"`(page-1) * limit` to `page * limit`, with `total` count"* — the rest of this README is decoration.

---

## 📑 Table of Contents

- [🧠 The One-Sentence Summary](#-the-one-sentence-summary)
- [📖 The Story: The Photo Album](#-the-story-the-photo-album)
- [🎯 What You Will Learn (10 Skills)](#-what-you-will-learn-10-skills)
- [📂 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#-installation--setup)
- [🧬 Anatomy of `main.py` — Line by Line (Heavily Commented)](#-anatomy-of-mainpy--line-by-line-heavily-commented)
- [🛣️ API Endpoints](#-api-endpoints)
- [🧠 The Mental Model: Offset-Limit Pagination](#-the-mental-model-offset-limit-pagination)
- [🆕 Every New Keyword Explained](#-every-new-keyword-explained)
- [🆚 Offset vs Cursor vs Page-Number](#-offset-vs-cursor-vs-page-number)
- [🆚 `page=N` vs `page[N]` vs `?page=1&size=5`](#-pagen-vs-page-n-vs-page1size5)
- [🧪 Try It With curl](#-try-it-with-curl)
- [🔧 Variations](#-variations)
- [⚠️ Common Pitfalls & Fixes](#-common-pitfalls--fixes)
- [🧠 Mnemonic Cheat Sheet](#-mnemonic-cheat-sheet)
- [🧪 Recall Test](#-recall-test)
- [🎯 Interview Q&A](#-interview-qa)
- [🚀 Where to Go Next](#-where-to-go-next)

---

## 📖 The Story: The Photo Album 📚

Imagine a photo album with **100 photos** on one shelf. Showing all 100 to a guest is a mess. Instead:

> "Here's **page 1** (photos 1–5). Flip the page for the next five."

That's **pagination**: split a big list into bite-sized chunks, delivered one page at a time.

```
[1 2 3 4 5]   ← page 1, limit 5
[6 7 8 9 10]  ← page 2, limit 5
[11 12 13 14 15] ← page 3, limit 5
...
```

> 🧠 **Mnemonic:** "*`(page-1) * limit` is the first photo; `page * limit` is just past the last.*"

---

## 🎯 What You Will Learn (10 Skills)

| # | 🎯 Skill | 🧠 You'll remember it because... |
|:-:|:---------|:--------------------------------|
| 1 | 📑 **Offset-limit pattern** | "`skip` and `take`" |
| 2 | 📐 **`start = (page-1) * limit`** | "Where this page begins" |
| 3 | 📏 **`end = start + limit`** | "Where this page ends" |
| 4 | 📊 **`len(items)` for `total`** | "The grand total" |
| 5 | 🔪 **`items[start:end]`** | "The current slice" |
| 6 | 📝 **Query params `page` / `limit`** | Defaults via `= 1` / `= 5` |
| 7 | 🌀 **404 on empty page** | "If the slice is empty" |
| 8 | 🔢 **1-indexed vs 0-indexed** | "`page=1` is human-friendly" |
| 9 | 🔒 **`limit` cap** | "Don't hand out 10k rows" |
| 10 | 📡 **Pagination metadata** | `{page, limit, total, data}` |

---

## 📂 Project Structure

```
📁 A030_Pagination_Explained_Limit_Real_API_Example/
├── 🐍 main.py      ← 45 lines: crawl HN + paginate
├── 📦 requirements.txt ← fastapi[standard] + requests + beautifulsoup4
└── 📖 README.md    ← you are here
```

---

## ⚙️ Installation & Setup

```powershell
cd "D:\AllProgram\LEARN\Python\FastAPI\A030_Pagination_Explained_Limit_Real_API_Example"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

> ⚠️ Crawls `https://news.ycombinator.com/` — needs network access and the CSS class names may change.

---

## 🧬 Anatomy of `main.py` — Line by Line (Heavily Commented)

The full file is now annotated (code logic unchanged, comments added). Here's the **pagination** portion:

```python
# =========================================================
# GET /news  —  crawl HN + paginate the results
# =========================================================
# Query parameters:
#   page  (int, default 1)  → which page of results to return
#   limit (int, default 5)  → items per page
@app.get("/news")
def get_news(page: int = 1, limit: int = 5):
    # 1. The upstream page we crawl (Hacker News front page)
    url = "https://news.ycombinator.com/"

    # 2. Fetch the raw HTML
    response = requests.get(url)

    # 3. Parse the HTML into a searchable tree
    soup = BeautifulSoup(response.text, "html.parser")

    # 4. Extract all titles
    titles = []
    for item in soup.find_all("span", class_="titleline"):
        titles.append(item.text)

    # 5. Pagination: slice the full list
    #    `start` = where this page begins
    #    `end`   = where it ends
    #    e.g. page=2, limit=5 → start=5, end=10
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(titles),       # total matching items
        "data": titles[start:end]   # the current page of results
    }
```

| Line | Code | 🧠 Why it's there |
|:----:|:-----|:------------------|
| 8 | `page: int = 1, limit: int = 5` | Query params with defaults |
| 21 | `start = (page - 1) * limit` | 0-indexed start of the slice |
| 22 | `end = start + limit` | end index (exclusive) |
| 24–27 | `return {page, limit, total, data}` | Pagination envelope |

### The Magic Formula

```python
start = (page - 1) * limit     # e.g. page 3, limit 5 → start = 10
end = start + limit            # end = 15
titles[start:end]              # items 10, 11, 12, 13, 14
```

### 🎯 If you remember ONE thing
> **`start = (page-1) * limit`, `end = start + limit`, slice `[start:end]`, return `{page, limit, total, data}`.**

---

## 🛣️ API Endpoints

| Method | Endpoint | Returns |
|:------:|:---------|:--------|
| 🟢 GET | `/news` | `{page, limit, total, data}` |
| 🟢 GET | `/news?page=2` | Page 2 |
| 🟢 GET | `/news?page=2&limit=10` | 10 items from page 2 |

---

## 🧠 The Mental Model: Offset-Limit Pagination

```mermaid
flowchart LR
    A[title[0..99)] --> B["start=(page-1)*limit"]
    B --> C["end=start+limit"]
    C --> D["slice = title[start:end]"]
    D --> E["return {page, limit, total, data: slice}"]
```

Example for `GET /news?page=3&limit=5`:

```
titles = [t0, t1, t2, t3, t4, t5, t6, ..., t99]
                |--- page 1 ---|  |--- page 2 ---|  |--- page 3 ---|
                              ^10              ^15               ^20
start = (3-1) * 5 = 10
end   = 10 + 5 = 15
slice = titles[10:15] = [t10, t11, t12, t13, t14]
```

> 🧠 **`page` is 1-indexed (for humans). Python slicing is 0-indexed. The formula bridges the gap.**

---

## 🆕 Every New Keyword Explained

### 1. Pagination

**What:** Splitting a large result set into smaller, fixed-size chunks ("pages") so clients aren't overwhelmed and the server isn't overloaded.

> 🧠 **Mnemonic:** "**Pagination = many pages, one small slice per request.**"

### 2. Offset

**What:** The number of items to skip from the start before taking the slice. In SQL: `OFFSET n`. In Python: `list[n:n+limit]`.

```python
offset = (page - 1) * limit
```

> 🧠 **Mnemonic:** "**Offset = how many to jump over.**"

### 3. Limit

**What:** The maximum number of items to return per page.

```python
items[0:limit]     # the first `limit` items
```

> 🧠 **Mnemonic:** "**Limit = how many to take.**"

### 4. `page: int = 1` — query parameter with default

**What:** FastAPI reads `page` from the URL (e.g. `/news?page=3`). The `= 1` is the default applied when the client omits the parameter.

```python
@app.get("/news")
def get_news(page: int = 1, limit: int = 5):
    ...
```

> 🧠 **Mnemonic:** "**`= default` is applied when the client doesn't send the param.**"

### 5. `start:end` — slice

**What:** Python slicing syntax. `titles[start:end]` returns items from `start` to `end - 1`. If `start` is beyond the list, returns `[]`.

```python
titles[10:15]    # items 10, 11, 12, 13, 14
titles[100:105]  # []  (nothing there)
```

> 🧠 **Mnemonic:** "**Slice doesn't crash. It just gives you what's left.**"

### 6. `len(titles)` — total count

**What:** The total number of **matching** items (before pagination). Returned to the client so it knows how many pages exist.

```python
return {"total": len(titles), "data": titles[start:end]}
```

> 🧠 **Mnemonic:** "**`total` = all matches. `data` = this page of matches.**"

### 7. 1-indexed vs 0-indexed

**What:** `page=1` means "the first page" (human-friendly, 1-indexed). But Python lists start at index 0. The formula `(page-1) * limit` translates.

| Page | 1-indexed | `(page-1)*limit` (0-indexed offset) |
|:-----|:----------|:------------------------------------|
| 1 | "first page" | 0 |
| 2 | "second page" | `limit` |
| 3 | "third page" | `2 * limit` |

> 🧠 **Mnemonic:** "**`page - 1` bridges human (1-indexed) and Python (0-indexed).**"

### 8. Pagination envelope

**What:** The response shape: `{page, limit, total, data}`. This tells the client everything it needs to build a UI.

| Field | Meaning |
|:------|:--------|
| `page` | Which page was returned |
| `limit` | How many items per page |
| `total` | How many items **total** |
| `data` | The items for this page |

> 🧠 **Mnemonic:** "**Envelope = page + limit + total + data.**"

### 9. Cursor pagination (the modern alternative)

**What:** Instead of offset/limit, pass a "cursor" (the ID or timestamp of the last item). More stable under inserts.

```python
@app.get("/items")
def list_items(cursor: str | None = None, limit: int = 5):
    ...
    items, next_cursor = db.query_after_cursor(cursor, limit)
    return {"data": items, "next_cursor": next_cursor, "has_more": len(items) == limit}
```

> 🧠 **Mnemonic:** "**Cursor = 'give me what comes after this'.**"

### 10. `limit` cap

**What:** Clamp `limit` to a reasonable maximum so a client can't request all rows at once.

```python
limit = min(limit, 100)
```

> 🧠 **Mnemonic:** "**Cap the limit. 10000 rows kills your server.**"

---

## 🆚 Offset vs Cursor vs Page-Number

| Strategy | How it works | Good for | Bad for |
|:---------|:-------------|:---------|:--------|
| Offset (`page=N&limit=L`) | `LIMIT L OFFSET (N-1)*L` | Admin UIs, stable data | Slow on large offsets; shifts on inserts |
| Cursor (`?cursor=ID&limit=L`) | `WHERE id > cursor LIMIT L` | Infinite scroll, feeds | Random access (page 50) is hard |
| Page-number (`?page=N&size=L`) | Offset underneath | Human-friendly URLs | Same issues as offset |

> 🧠 **Mnemonic:** "**Offset = easy but shifts. Cursor = stable but no random access.**"

---

## 🆚 `page=N` vs `page[N]` vs `?page=1&size=5`

| Style | Example |
|:------|:--------|
| Query param (this module) | `GET /news?page=2&limit=5` |
| Path param | `GET /news/page/2` |
| Query with `size` instead of `limit` | `GET /news?page=2&size=5` |
| Nested array in query | `GET /news?page[2]` (rare) |
| Matrix params (rare) | `GET /news;page=2;limit=5` |

> 🧠 **Mnemonic:** "**Query params (`page=` `limit=`) are the common idiom.**"

---

## 🧪 Try It With curl

### 1. Page 1, default limit (5)

```bash
curl "http://127.0.0.1:8000/news"
```

```json
{
  "page": 1,
  "limit": 5,
  "total": 30,
  "data": ["Title 1", "Title 2", "Title 3", "Title 4", "Title 5"]
}
```

### 2. Page 2, limit 3

```bash
curl "http://127.0.0.1:8000/news?page=2&limit=3"
```

```json
{
  "page": 2,
  "limit": 3,
  "total": 30,
  "data": ["Title 4", "Title 5", "Title 6"]
}
```

### 3. Page beyond the data

```bash
curl "http://127.0.0.1:8000/news?page=99&limit=5"
```

```json
{
  "page": 99,
  "limit": 5,
  "total": 30,
  "data": []    # empty — no crash
}
```

### 4. Negative page (FastAPI still accepts it; returns empty)

```bash
curl "http://127.0.0.1:8000/news?page=-1&limit=5"
```

```json
{"page": -1, "limit": 5, "total": 30, "data": []}
```

---

## 🔧 Variations

### Variation 1: Cap the limit

```python
@app.get("/news")
def get_news(page: int = 1, limit: int = 5):
    limit = min(limit, 50)    # never return more than 50
    ...
```

### Variation 2: Use `skip` + `limit` (SQL-style)

```python
@app.get("/news")
def get_news(skip: int = 0, limit: int = 5):
    data = titles[skip:skip + limit]
    return {"skip": skip, "limit": limit, "total": len(titles), "data": data}
```

### Variation 3: Return 404 on an empty page

```python
@app.get("/news")
def get_news(page: int = 1, limit: int = 5):
    if page < 1:
        raise HTTPException(400, "page must be >= 1")
    start = (page - 1) * limit
    end = start + limit
    data = titles[start:end]
    if page > 1 and not data:
        raise HTTPException(404, "Page out of range")
    return {"page": page, "limit": limit, "total": len(titles), "data": data}
```

### Variation 4: SQLAlchemy with offset + limit

```python
@app.get("/todos")
def list_todos(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    todos = db.query(Todo).offset(skip).limit(limit).all()
    total = db.query(Todo).count()
    return {"skip": skip, "limit": limit, "total": total, "data": todos}
```

### Variation 5: Cursor-based pagination

```python
@app.get("/items")
def list_items(after: int | None = None, limit: int = 5):
    query = db.query(Item).order_by(Item.id)
    if after is not None:
        query = query.filter(Item.id > after)
    items = query.limit(limit + 1).all()
    has_more = len(items) > limit
    items = items[:limit]
    return {
        "data": items,
        "has_more": has_more,
        "next_cursor": items[-1].id if items else None,
    }
```

---

## ⚠️ Common Pitfalls & Fixes

| 😖 Pitfall | 🔍 Cause | ✅ Fix |
|:-----------|:---------|:------|
| Empty page returns 200 with `[]` | Expected 404 | Add `if not data and page > 1: raise HTTPException(404)` |
| `page=-1` gives weird results | No bounds check | `if page < 1: raise HTTPException(400)` |
| `limit=0` hangs | Slice with step 0 | Guard: `limit = max(1, min(limit, 100))` |
| `limit=99999999` OOMs the server | No cap | Cap at a max (100, 1000) |
| Off-by-one: page 2 starts at wrong index | `page * limit` instead of `(page-1) * limit` | Always use `(page - 1) * limit` |
| Client can't tell if it's the last page | No `total` or `has_more` | Return both |
| 422 on `page=1.5` | FastAPI coerces to int | That's correct — let it reject floats |

### The "No limit cap" Trap

```python
# ❌ A client requests a million items — server OOMs
@app.get("/news")
def get_news(limit: int = 5):
    return titles[:limit]   # limit = 1,000,000 → crash

# ✅ Cap it
@app.get("/news")
def get_news(limit: int = 5):
    limit = min(limit, 100)
    return titles[:limit]
```

### The "Negative page" Trap

```python
# ❌ page=-1 → start=-5 → returns the last 5 items (weird)
@app.get("/news")
def get_news(page: int = 1):
    start = (page - 1) * limit    # (0) * 5 = 0
    ...

# ✅ Guard it
@app.get("/news")
def get_news(page: int = 1):
    if page < 1:
        raise HTTPException(status_code=400, detail="page must be >= 1")
```

### The "Off-by-one" Trap

```
page 1: items [0:5]  → correct
page 2: items [5:10] → correct   (start = (2-1)*5 = 5)
page 3: items [10:15] → correct  (start = (3-1)*5 = 10)

WRONG: start = page * limit
page 1: [5:10]  ← wrong!
page 2: [10:15] ← wrong!
```

> 🧠 **Mnemonic:** "**`(page-1) * limit`. Not `page * limit`.**"

---

## 🧠 Mnemonic Cheat Sheet

| Concept | Mnemonic | Story |
|:--------|:---------|:------|
| 3-step flow | **S-L-T** | Start, Length, Total |
| Start index | `(page-1) * limit` | Bridge 1-indexed page ↔ 0-indexed slice |
| End index | `start + limit` | Exclusive |
| `total` | `len(items)` | Grand total |
| `data` | `items[start:end]` | This page |
| `page` default | `= 1` | Humans start counting at 1 |
| `limit` default | `= 5` | A small, friendly page size |
| Empty page | "No crash" | Slice returns `[]` |
| Limit cap | `min(limit, 100)` | Don't hand out 10k |
| Cursor | "after this ID" | For infinite scroll |
| Offset | "skip N" | SQL `OFFSET N` |

---

## 🧪 Recall Test

1. How do you compute the start index for a page?
2. How do you compute the end index?
3. What's the difference between `total` and `len(data)`?
4. How do you return a slice in Python?
5. What happens if the client requests `page=99` of 10 pages?
6. Should you cap `limit`?
7. Why is `(page-1) * limit` correct but `page * limit` wrong?
8. When would you use cursor pagination instead of offset-limit?

> 8/8 → pagination is yours.

---

## 🎯 Interview Q&A

### Q1: Explain offset-limit pagination.

**Answer:** A "page" is a slice of results. Given `page` (1-indexed) and `limit` (items per page):

- `start = (page - 1) * limit`
- `end = start + limit`
- `data = items[start:end]`

Return `{page, limit, total, data}` so the client can build a UI.

> **One-liner:** *"`(page-1)*limit` to `page*limit`, return the slice + total.**"*

### Q2: Why `(page - 1)` and not `page`?

**Answer:** Because pages are 1-indexed (page 1 is the first page) but Python lists are 0-indexed (index 0 is the first item). Subtracting 1 bridges the two.

```
page 1 → start = 0       → items[0:5]
page 2 → start = 5       → items[5:10]
page 3 → start = 10      → items[10:15]
```

> **One-liner:** *"1-indexed page, 0-indexed list. Page − 1 bridges them.*

### Q3: Should you cap the `limit`? Why?

**Answer:** Yes. A client can request `limit=9999999`, which would try to return a million rows and exhaust memory.

```python
@app.get("/news")
def get_news(limit: int = 5):
    limit = min(limit, 100)    # hard cap at 100
```

> **One-liner:** *"Cap the limit. 10000 rows kills the server.*

### Q4: What should you return for an empty page?

**Answer:** Two valid options:

1. **200 with `"data": []`** — "the page is valid; here's an empty list" (common in APIs like Stripe)
2. **404** — "that page doesn't exist" — useful if `page > max_possible_page`

The key is to be **consistent** and include `total` so the client can compute which is the last page.

> **One-liner:** *"Empty page: 200 `[]` is most common. Return `total` so the client can tell.*

### Q5: What's the difference between offset and cursor pagination?

**Answer:**

| Offset (`page=N&limit=L`) | Cursor (`after=ID&limit=L`) |
|:-------------------------|:----------------------------|
| `LIMIT L OFFSET (N-1)*L` | `WHERE id > after LIMIT L` |
| Can jump to any page | Must go in order |
| Shifts when items are inserted/deleted | Stable under inserts/deletes |
| Easy UI (numbered page buttons) | Better for infinite scroll |

> **One-liner:** *"Offset = easy but shifts. Cursor = stable but no random access.*

### Q6: How would you paginate a database query?

**Answer:** With SQLAlchemy, use `offset()` and `limit()`:

```python
items = db.query(Item).offset(skip).limit(limit).all()
total = db.query(Item).count()    # extra query, but worth it
return {"skip": skip, "limit": limit, "total": total, "data": items}
```

> **One-liner:** *"`.offset(skip).limit(limit).all()` + `.count()`."

### Q7: What metadata fields should a paginated response include?

**Answer:** At minimum, the response should include:

- `page` — the current page number
- `limit` — the items-per-page value
- `total` — the total number of items (before pagination)
- `data` — the list of items for this page
- (Bonus) `has_more` or `next_page` — to simplify client logic

> **One-liner:** *"page, limit, total, data — the standard envelope.*

### Q8: When would `page=2&limit=5` return fewer than 5 items?

**Answer:** Two cases:

1. The last page — there are fewer remaining items than `limit`.
2. There are **zero** items on that page (page is beyond the data).

In both cases the response is still valid: 200 with `"data": [...]` (possibly `[]`).

> **One-liner:** *"Last page or beyond — `data` is shorter or empty. That's not an error.*

---

## 🚀 Where to Go Next

| Direction | Module |
|:----------|:-------|
| ⬅️ Previous | [A029](../A029_Web_Crawling_Requests_BeautifulSoup_Fetch_Website_Data/) |
| ⬅️ Back | [Root README](../README.md) |
| ➡️ Next | A031 (planned) — Cursor-based pagination with `after` token |
| ➡️ Future | A032 (planned) — Paginated + filtered APIs |

---

<div align="center">

### 📄 *Slice the list. Return the page. Tell them the total.* 📄

Made with ❤️, `titles[start:end]`, and `{"page", "limit", "total", "data"}`.

</div>