# =========================================================
# A030 — Pagination Explained (Limit) + Real API Example
# =========================================================
# Combines two concepts:
#   1. Web crawling      → fetches Hacker News (https://news.ycombinator.com)
#                            and extracts titles using BeautifulSoup
#   2. Pagination        → slices the title list with `page` and `limit`
#                            query parameters, and returns page/limit/total
#
# Route:
#   - GET /news?page=1&limit=5  → returns 5 titles from page 1, plus metadata
# =========================================================

# --- FastAPI: framework ---
from fastapi import FastAPI

# --- requests: fetch the upstream HTML ---
import requests

# --- BeautifulSoup: parse HTML + extract titles ---
from bs4 import BeautifulSoup

# 1. Create the FastAPI app instance
app = FastAPI()


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

    # 2. Fetch the raw HTML (note: no timeout in the original code — see README)
    response = requests.get(url)

    # 3. Parse the HTML into a searchable tree
    soup = BeautifulSoup(response.text, "html.parser")

    # 4. Extract all titles (HN uses <span class="titleline"> for each story)
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
