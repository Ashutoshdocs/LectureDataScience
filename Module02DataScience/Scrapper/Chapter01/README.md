# Web Scraping Demo (Python)

A beginner-friendly example that collects quotes from
[quotes.toscrape.com](https://quotes.toscrape.com) — a site built for practicing scraping —
and saves them to a CSV file.

---

## What is web scraping?

Web scraping means **using a program to read a web page and pull out the information you need**,
instead of copying it by hand.

Every web page is just text written in **HTML**. HTML wraps content in *tags*, like this:

```html
<div class="quote">
    <span class="text">"The world as we have created it is a process of our thinking."</span>
    <small class="author">Albert Einstein</small>
</div>
```

A scraper downloads that HTML, finds the tags it cares about (e.g. `<small class="author">`),
and grabs the text inside them.

---

## The 4 basic steps

| Step | What happens | Tool used |
|------|--------------|-----------|
| 1. Download | Fetch the page's HTML from the internet | `requests` |
| 2. Parse | Turn the HTML text into something searchable | `BeautifulSoup` |
| 3. Extract | Find the tags and pull out the text | `find()` / `find_all()` |
| 4. Save | Store the results in a file | `csv` |

---

## Setup

1. Make sure Python 3 is installed:
   ```bash
   python --version
   ```

2. Install the two libraries:
   ```bash
   pip install requests beautifulsoup4
   ```

3. Run the script:
   ```bash
   python scraper.py
   ```

### Expected output

```
Downloading: https://quotes.toscrape.com
  Page 1: found 10 quotes
Downloading: https://quotes.toscrape.com/page/2/
  Page 2: found 10 quotes

First 3 quotes:
  "The world as we have created it is a process of our thinking..."  - Albert Einstein
  ...
Saved 20 quotes to quotes.csv
```

A file called `quotes.csv` appears in the same folder. Open it in Excel or Google Sheets.

---

## How the code works

### 1. Downloading a page — `get_page()`

```python
response = requests.get(url, headers=HEADERS, timeout=10)
response.raise_for_status()
return response.text
```

- `requests.get()` visits the URL, just like a browser.
- `headers` sends a **User-Agent** so the site knows who's visiting.
- `timeout=10` stops waiting after 10 seconds.
- `raise_for_status()` raises an error if the page failed (e.g. 404).
- `response.text` is the raw HTML.

### 2 & 3. Parsing and extracting — `parse_quotes()`

```python
soup = BeautifulSoup(html, "html.parser")

for block in soup.find_all("div", class_="quote"):
    text   = block.find("span",  class_="text").get_text(strip=True)
    author = block.find("small", class_="author").get_text(strip=True)
```

- `BeautifulSoup(...)` turns HTML into a searchable object.
- `find_all("div", class_="quote")` → **every** quote box on the page.
- `find("span", class_="text")` → the **first** matching tag inside that box.
- `get_text(strip=True)` → just the text, with extra spaces removed.

> `class_` has an underscore because `class` is a reserved word in Python.

### Following to the next page — `get_next_page_url()`

The site shows 10 quotes per page with a **Next →** button. The script finds that button's link
(`/page/2/`), adds it to the base URL, and repeats. It stops after `PAGES_TO_SCRAPE` pages
or when there's no Next button.

### 4. Saving — `save_to_csv()`

```python
writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
writer.writeheader()
writer.writerows(quotes)
```

Each quote is a dictionary, and `DictWriter` turns each one into a row of the CSV.

---

## How do I know which tags to look for?

1. Open the website in Chrome or Firefox.
2. Right-click on the thing you want (e.g. an author name) → **Inspect**.
3. The developer panel highlights its HTML, e.g. `<small class="author">`.
4. Use that tag name and class in `find()` / `find_all()`.

---

## Try it yourself

- Change `PAGES_TO_SCRAPE` to `5` to collect more quotes.
- Print only quotes by a certain author:
  ```python
  einstein = [q for q in all_quotes if q["author"] == "Albert Einstein"]
  ```
- Point the scraper at [books.toscrape.com](https://books.toscrape.com) and extract book titles and prices instead.

---

## Scraping responsibly

- **Check `robots.txt`** (e.g. `https://example.com/robots.txt`) to see what a site allows.
- **Read the site's Terms of Service** — some sites forbid scraping.
- **Go slow.** The script waits 1 second between pages (`time.sleep(1)`) so it doesn't overload the server.
- **Prefer an official API** if the site offers one.
- **Don't collect personal data** without permission.

---

## Common problems

| Problem | Likely cause |
|---------|--------------|
| `ModuleNotFoundError: No module named 'bs4'` | Run `pip install beautifulsoup4` |
| `AttributeError: 'NoneType' object has no attribute 'get_text'` | The tag wasn't found — the site's HTML changed or the class name is wrong |
| Empty results | The page loads content with JavaScript; `requests` only sees the initial HTML (tools like Selenium or Playwright handle this) |
| `403 Forbidden` | The site is blocking scrapers — respect that |
