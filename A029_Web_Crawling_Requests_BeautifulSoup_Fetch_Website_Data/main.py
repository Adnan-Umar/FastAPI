# =========================================================
# A029 — Web Crawling with requests + BeautifulSoup
# =========================================================
# A FastAPI route that fetches a live news page with `requests`,
# parses the HTML with BeautifulSoup, and returns the article
# headlines as JSON.
#
# Example route:
#   - GET /news → fetches https://indianexpress.com/,
#     extracts titles from `<a class="topblockNews__sidebarLink">`,
#     returns {"news": ["headline1", "headline2", ...]}
# =========================================================

# --- FastAPI: framework + HTTP error handling ---
from fastapi import FastAPI, HTTPException

# --- `requests`: fetch the upstream HTML page ---
import requests

# --- `beautifulsoup4`: parse the HTML and extract headlines ---
# `bs4.BeautifulSoup` builds a parse tree from raw HTML.
from bs4 import BeautifulSoup

# 1. Create the FastAPI app instance
app = FastAPI()


# =========================================================
# GET /news  —  crawl + parse a news site
# =========================================================
@app.get("/news")
def get_news():
    # The page we want to scrape (a real news site).
    url = "https://indianexpress.com/"

    # 1. Fetch the raw HTML. Always set a timeout.
    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as exc:
        raise HTTPException(502, f"Failed to fetch upstream: {exc}")

    # 2. Check the HTTP status before parsing
    if response.status_code != 200:
        raise HTTPException(
            502,
            f"Upstream returned HTTP {response.status_code}"
        )

    # 3. Parse the HTML into a searchable tree.
    #    "html.parser" is the stdlib parser bundled with Python.
    soup = BeautifulSoup(response.text, "html.parser")

    # 4. Extract headlines.
    #    ⚠️  CSS selectors are FRAGILE: if the site changes its class names,
    #    this will return an empty list. That's a fact of life with scraping.
    titles = []
    for item in soup.find_all("a", class_="topblockNews__sidebarLink"):
        # `.strip()` removes leading/trailing whitespace from the headline text
        titles.append(item.text.strip())

    return {
        "news": titles
    }
