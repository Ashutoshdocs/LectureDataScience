"""
Simple Web Scraping Demo
========================

This script scrapes quotes from https://quotes.toscrape.com
(a website made specifically for practicing web scraping).

It shows the 4 basic steps of web scraping:
    1. Download a web page        -> requests
    2. Parse the HTML             -> BeautifulSoup
    3. Extract the data you want  -> find() / find_all()
    4. Save the data              -> csv

Run it with:
    python scraper.py
"""

import csv
import time

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------
# Settings
# ---------------------------------------------------------------
BASE_URL = "https://quotes.toscrape.com"
PAGES_TO_SCRAPE = 2              # keep it small and polite
OUTPUT_FILE = "quotes.csv"

# A "User-Agent" tells the website what kind of program is visiting.
# Some sites block requests that don't send one.
HEADERS = {"User-Agent": "Mozilla/5.0 (learning web scraping demo)"}


# ---------------------------------------------------------------
# Step 1: Download the page
# ---------------------------------------------------------------
def get_page(url):
    """Download a web page and return its HTML as text."""
    print(f"Downloading: {url}")
    response = requests.get(url, headers=HEADERS, timeout=10)

    # Stop if something went wrong (e.g. 404 Not Found, 500 Server Error)
    response.raise_for_status()

    return response.text


# ---------------------------------------------------------------
# Step 2 + 3: Parse the HTML and extract data
# ---------------------------------------------------------------
def parse_quotes(html):
    """Turn raw HTML into a list of dictionaries (one per quote)."""
    soup = BeautifulSoup(html, "html.parser")
    quotes = []

    # Every quote on the page lives inside: <div class="quote"> ... </div>
    for block in soup.find_all("div", class_="quote"):
        text = block.find("span", class_="text").get_text(strip=True)
        author = block.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in block.find_all("a", class_="tag")]

        quotes.append({
            "text": text,
            "author": author,
            "tags": ", ".join(tags),
        })

    return quotes


def get_next_page_url(html):
    """Find the 'Next' button link, or return None if there isn't one."""
    soup = BeautifulSoup(html, "html.parser")
    next_button = soup.find("li", class_="next")

    if next_button:
        relative_link = next_button.find("a")["href"]   # e.g. "/page/2/"
        return BASE_URL + relative_link
    return None


# ---------------------------------------------------------------
# Step 4: Save the data
# ---------------------------------------------------------------
def save_to_csv(quotes, filename):
    """Write the list of quotes to a CSV file (opens in Excel)."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
        writer.writeheader()
        writer.writerows(quotes)
    print(f"Saved {len(quotes)} quotes to {filename}")


# ---------------------------------------------------------------
# Main program: put all the steps together
# ---------------------------------------------------------------
def main():
    all_quotes = []
    url = BASE_URL

    for page_number in range(1, PAGES_TO_SCRAPE + 1):
        if url is None:          # no more pages left
            break

        try:
            html = get_page(url)
        except requests.RequestException as error:
            print(f"Could not download page: {error}")
            break

        quotes = parse_quotes(html)
        print(f"  Page {page_number}: found {len(quotes)} quotes")
        all_quotes.extend(quotes)

        url = get_next_page_url(html)
        time.sleep(1)            # be polite: wait 1 second between requests

    # Show a small preview in the terminal
    print("\nFirst 3 quotes:")
    for q in all_quotes[:3]:
        print(f'  {q["text"]}  - {q["author"]}')

    if all_quotes:
        save_to_csv(all_quotes, OUTPUT_FILE)


if __name__ == "__main__":
    main()
