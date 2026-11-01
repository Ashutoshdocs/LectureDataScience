"""
Scrape Our Own Web Page with requests
=====================================

This script:
    1. Starts a tiny web server on your computer that serves shop.html
    2. Downloads the page with `requests` (just like a real website)
    3. Reads the HTML with BeautifulSoup
    4. Extracts every fruit and the deals table
    5. Prints a summary and saves everything to fruits.csv

Install:
    pip install requests beautifulsoup4

Run (from inside this folder):
    python scrape_shop.py
"""

import csv
import http.server
import os
import threading

import requests
from bs4 import BeautifulSoup

PORT = 8000
URL = f"http://localhost:{PORT}/shop.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (learning web scraping demo)"}


# ---------------------------------------------------------------
# Step 0: Start a local web server
# ---------------------------------------------------------------
def start_server():
    """
    Serve the files in this folder at http://localhost:8000
    so `requests` can download shop.html exactly like a real site.

    This does the same thing as running:  python -m http.server 8000
    """
    folder = os.path.dirname(os.path.abspath(__file__))

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=folder, **kwargs)

        def log_message(self, format, *args):
            pass   # hide the server's log lines to keep output clean

    server = http.server.ThreadingHTTPServer(("localhost", PORT), QuietHandler)

    # Run the server in the background so the rest of the script can continue
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Local server running at http://localhost:{PORT}")
    return server


# ---------------------------------------------------------------
# Step 1: Download the page with requests
# ---------------------------------------------------------------
def download_page(url):
    print(f"\nDownloading {url} ...")
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()              # stop if we got 404, 500, etc.

    response.encoding = "utf-8"              # so ₹ and emoji show correctly
    print(f"Status code : {response.status_code}")
    print(f"Page size   : {len(response.text):,} characters")
    return response.text


# ---------------------------------------------------------------
# Step 2: Small helper to turn "₹450" into the number 450
# ---------------------------------------------------------------
def to_number(price_text):
    digits = "".join(ch for ch in price_text if ch.isdigit())
    return int(digits) if digits else 0


# ---------------------------------------------------------------
# Step 3: Extract the fruits
# ---------------------------------------------------------------
def extract_fruits(soup):
    fruits = []

    # Each fruit lives in: <article class="product" data-id="..." data-category="...">
    for card in soup.find_all("article", class_="product"):

        # The price tag holds "₹450 <small>/ dozen</small>".
        # We read the small "unit" part, then the number on its own.
        price_tag = card.find("span", class_="price")
        unit = price_tag.find("small").get_text(strip=True).replace("/", "").strip()
        price = to_number(price_tag.contents[0])     # first piece = "₹450 "

        # A badge only exists on some cards, so check before using it
        badge_tag = card.find("span", class_="badge")
        badge = badge_tag.get_text(strip=True) if badge_tag else ""

        fruits.append({
            "id":          card["data-id"],                    # read an attribute
            "name":        card.find("h3", class_="name").get_text(strip=True),
            "category":    card["data-category"],
            "origin":      card.find("p", class_="origin").get_text(strip=True),
            "price":       price,
            "unit":        unit,
            "rating":      float(card.find("span", class_="rating")["data-rating"]),
            "in_stock":    "in-stock" in card.find("span", class_="stock")["class"],
            "badge":       badge,
            "link":        card.find("a", class_="buy")["href"],
        })

    return fruits


# ---------------------------------------------------------------
# Step 4: Extract the deals table
# ---------------------------------------------------------------
def extract_deals(soup):
    deals = []
    table = soup.find("table", id="deals-table")

    for row in table.find("tbody").find_all("tr"):
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        deals.append({
            "fruit":     cells[0],
            "old_price": to_number(cells[1]),
            "new_price": to_number(cells[2]),
            "discount":  cells[3],
        })

    return deals


# ---------------------------------------------------------------
# Step 5: Show results and save them
# ---------------------------------------------------------------
def show_results(page_title, fruits, deals):
    print(f"\nPage title  : {page_title}")

    print(f"\n{'FRUIT':<28}{'PRICE':>8}  {'UNIT':<8}{'RATING':>7}  STOCK")
    print("-" * 62)
    for f in fruits:
        stock = "yes" if f["in_stock"] else "NO"
        print(f"{f['name']:<28}{'₹' + str(f['price']):>8}  {f['unit']:<8}{f['rating']:>7}  {stock}")

    # A little analysis, now that the data is in Python
    best = max(fruits, key=lambda f: f["rating"])
    in_stock = [f for f in fruits if f["in_stock"]]
    print(f"\nTotal fruits     : {len(fruits)}")
    print(f"In stock         : {len(in_stock)}")
    print(f"Highest rated    : {best['name']} ({best['rating']})")

    print("\nToday's deals:")
    for d in deals:
        print(f"  {d['fruit']:<20} ₹{d['old_price']} -> ₹{d['new_price']}  ({d['discount']} off)")


def save_csv(fruits, filename="fruits.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fruits[0].keys())
        writer.writeheader()
        writer.writerows(fruits)
    print(f"\nSaved {len(fruits)} fruits to {filename}")


# ---------------------------------------------------------------
# Main program
# ---------------------------------------------------------------
def main():
    server = start_server()
    try:
        html = download_page(URL)
        soup = BeautifulSoup(html, "html.parser")

        page_title = soup.title.get_text(strip=True)
        fruits = extract_fruits(soup)
        deals = extract_deals(soup)

        show_results(page_title, fruits, deals)
        save_csv(fruits)
    finally:
        server.shutdown()                    # always stop the server at the end
        print("Server stopped.")


if __name__ == "__main__":
    main()
