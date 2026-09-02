# =========================================================
# A031 — Caching Explained (TTL-based) + Boost API Performance
# =========================================================
# Combines two concepts:
#   1. Web crawling      → fetches Hacker News (https://news.ycombinator.com)
#                           and extracts titles using BeautifulSoup
#   2. TTL caching      → caches the scraped result for 60 seconds so we
#                           don't hit the upstream on every request
#
# Route:
#   - GET /news  → returns cached news (first call fetches, next 60s reuse)
#   - The response includes "time_taken" so you can see cache vs fresh
# =========================================================

# --- FastAPI: framework ---
from fastapi import FastAPI

# --- requests: fetch the upstream HTML ---
import requests

# --- BeautifulSoup: parse HTML + extract titles ---
from bs4 import BeautifulSoup

# --- stdlib: timers for TTL checks + timing ---
import time

# 1. Create the FastAPI app instance
app = FastAPI()

# =========================================================
# CACHE STORAGE
# =========================================================
# `cache_data`   — in-memory store of scraped titles (resets on restart)
# `last_fetch`   — epoch timestamp of the last upstream fetch (0 = "never fetched")
cache_data = []
last_fetch = 0

# Cache TTL (seconds) — how long to keep the cache fresh
CACHE_TTL_SECONDS = 60


@app.get("/news")
def get_news():
    # Make the module-level cache variables writable from inside the function
    global cache_data, last_fetch

    # Record the start time so we can report how long the request took
    start = time.time()

    # =========================================================
    # 1. CACHE CHECK — is the cache still within its TTL?
    # =========================================================
    # `time.time() - last_fetch` = seconds since the last fetch.
    # If that exceeds the TTL, the cache is STALE → fetch fresh data.
    # If `last_fetch == 0` (never fetched), this is also > TTL (60s),
    # so the first request ALWAYS fetches.
    if time.time() - last_fetch > CACHE_TTL_SECONDS:
        print("Fetching fresh data")

        # 1. The upstream page we crawl (Hacker News front page)
        url = "https://news.ycombinator.com/"

        # 2. Fetch the raw HTML
        #    (note: no explicit timeout in the original — see README Pitfalls)
        response = requests.get(url)

        # 3. Parse the HTML into a searchable tree
        soup = BeautifulSoup(response.text, "html.parser")

        # 4. Extract and cache all titles at once
        #    (HN uses <span class="titleline"> for each story)
        #    This overwrites the entire cache with fresh data.
        cache_data = [
            item.text for item in soup.find_all("span", class_="titleline")
        ]

        # 5. Stamp the cache with the current time so the next request
        #    can measure how old it is.
        last_fetch = time.time()
    else:
        print("Using Cache data")

    # =========================================================
    # 2. TIMING — report how long this request took
    # =========================================================
    # Cached requests are near-instant (microseconds).
    # Fresh requests include the upstream fetch + parse time.
    end = time.time()
    time_taken = round(end - start, 4)
    print("Time taken ", time_taken)

    # =========================================================
    # 3. RESPONSE — return the (up to) first 5 cached titles
    # =========================================================
    return {
        "time_taken": time_taken,    # in seconds; shows cache vs fresh
        "data": cache_data[:5]       # slice the first 5 headlines
    }
