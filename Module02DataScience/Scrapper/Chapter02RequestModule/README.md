# Scrape Your Own Web Page with Python 🍓

Learn web scraping safely by scraping a page **you own**.
This folder contains a colourful fruit-shop website and a Python script that downloads it
with `requests` and pulls out all the data with `BeautifulSoup`.

```
local_scraping_demo/
├── shop.html        ← the website (open it in your browser!)
├── scrape_shop.py   ← the scraper
└── README.md        ← this guide
```

---

## Why scrape a local page?

- **No internet needed**: it works offline.
- **Nothing can break**: real websites change their HTML and your scraper stops working. This one never changes.
- **No rules to worry about**: it's your own page, so there's no blocking, rate limits or terms of service.
- **You can see both sides**: you can read the HTML *and* the code that scrapes it.

---

## Quick start

1. Install the two libraries:
   ```bash
   pip install requests beautifulsoup4
   ```

2. Open `shop.html` in your browser to see the page you're about to scrape.

3. Run the scraper **from inside this folder**:
   ```bash
   cd local_scraping_demo
   python scrape_shop.py
   ```

### Expected output

```
Local server running at http://localhost:8000

Downloading http://localhost:8000/shop.html ...
Status code : 200
Page size   : 15,563 characters

Page title  : Tropicana Bazaar | Fresh Exotic Fruits

FRUIT                          PRICE  UNIT     RATING  STOCK
--------------------------------------------------------------
Alphonso Mango                  ₹450  dozen       4.9  yes
Dragon Fruit                    ₹180  piece       4.5  yes
Mahabaleshwar Strawberries      ₹220  box         4.7  yes
Nagpur Orange                   ₹120  kg          4.3  NO
...

Total fruits     : 8
In stock         : 6
Highest rated    : Alphonso Mango (4.9)

Today's deals:
  Alphonso Mango       ₹520 -> ₹450  (13% off)
  ...

Saved 8 fruits to fruits.csv
Server stopped.
```

A new file, `fruits.csv`, appears in the folder. Open it in Excel or Google Sheets.

---

## The big picture

```
 shop.html  ──►  local server  ──►  requests.get()  ──►  BeautifulSoup  ──►  Python data  ──►  fruits.csv
 (the page)     (localhost:8000)    (downloads HTML)     (searches HTML)    (lists/dicts)     (saved file)
```

| Step | What happens | Tool |
|------|--------------|------|
| 0 | Serve `shop.html` as a real web page | `http.server` (built into Python) |
| 1 | Download the page | `requests` |
| 2 | Turn HTML text into a searchable object | `BeautifulSoup` |
| 3 | Find the tags and pull out the text | `find()`, `find_all()` |
| 4 | Analyse and save the data | plain Python + `csv` |

---

## Step 0: Why do we need a server?

`requests` downloads pages from **URLs** (`http://...`). It can't open a file on your disk directly.

So the script starts a tiny web server that makes this folder available at:

```
http://localhost:8000/shop.html
```

`localhost` means "this computer". To `requests`, it behaves exactly like a real website.

> You can do the same thing yourself in a terminal with
> `python -m http.server 8000`, then visit `http://localhost:8000/shop.html` in your browser.

The server runs in a **background thread** so the rest of the script can keep going,
and `server.shutdown()` stops it at the end.

---

## Step 1: Downloading with `requests`

```python
response = requests.get(url, headers=HEADERS, timeout=10)
response.raise_for_status()
response.encoding = "utf-8"
html = response.text
```

| Line | What it does |
|------|--------------|
| `requests.get(url)` | Visits the URL, just like a browser |
| `headers=HEADERS` | Sends a User-Agent saying who is visiting |
| `timeout=10` | Gives up after 10 seconds instead of waiting forever |
| `raise_for_status()` | Raises an error if the page failed (404, 500…) |
| `response.encoding = "utf-8"` | Makes sure `₹` and emoji come through correctly |
| `response.text` | The page's HTML as one big string |

**Status codes to know:** `200` OK · `404` Not Found · `403` Forbidden · `500` Server Error

---

## Step 2: Understanding the HTML

Right-click any fruit card in your browser and choose **Inspect**. You'll see that every
fruit follows the same pattern:

```html
<article class="product" data-id="1" data-category="tropical">
  <span class="badge">Bestseller</span>
  <h3 class="name">Alphonso Mango</h3>
  <p class="origin">Ratnagiri, India</p>
  <div class="meta">
    <span class="price">₹450 <small>/ dozen</small></span>
    <span class="rating" data-rating="4.9">★ 4.9</span>
  </div>
  <span class="stock in-stock">In stock</span>
  <a class="buy" href="/fruit/alphonso-mango">Add to cart</a>
</article>
```

**This repeating pattern is what makes scraping possible.** Find one card, and you can
loop over all of them.

Words to know:

- **Tag**: the name in angle brackets: `article`, `h3`, `span`, `a`
- **Class**: a label for styling: `class="name"`. Your best friend when scraping.
- **Attribute**: extra info on a tag: `data-id="1"`, `href="/fruit/..."`
- **Text**: what's between the tags: `Alphonso Mango`

---

## Step 3: Extracting data with BeautifulSoup

### Finding every card

```python
soup = BeautifulSoup(html, "html.parser")

for card in soup.find_all("article", class_="product"):
    ...
```

`find_all()` returns **every** matching tag, so this loops 8 times, once per fruit.

### Getting text

```python
name = card.find("h3", class_="name").get_text(strip=True)
# "Alphonso Mango"
```

`find()` returns the **first** match *inside that card*. `get_text(strip=True)` gives the
text without extra spaces.

### Getting attributes

```python
card["data-id"]                                      # "1"
card["data-category"]                                # "tropical"
card.find("a", class_="buy")["href"]                 # "/fruit/alphonso-mango"
card.find("span", class_="rating")["data-rating"]    # "4.9"
```

Use square brackets, like a dictionary.

> **Tip:** `data-rating="4.9"` is cleaner than the visible text `★ 4.9`.
> Look for `data-` attributes; they often hold the raw values.

### Tags that might not exist

Only some fruits have a badge, so we check first:

```python
badge_tag = card.find("span", class_="badge")
badge = badge_tag.get_text(strip=True) if badge_tag else ""
```

If you skip this check, `find()` returns `None` and you'll get:
`AttributeError: 'NoneType' object has no attribute 'get_text'`

### Checking a class

```python
in_stock = "in-stock" in card.find("span", class_="stock")["class"]
# True or False
```

A tag's `class` is a list (e.g. `["stock", "in-stock"]`), so we check whether
`"in-stock"` is in it.

### Cleaning prices

The page shows `₹450`, but we want the number `450` so we can do maths with it:

```python
def to_number(price_text):
    digits = "".join(ch for ch in price_text if ch.isdigit())
    return int(digits) if digits else 0
```

### Scraping a table

```python
table = soup.find("table", id="deals-table")

for row in table.find("tbody").find_all("tr"):
    cells = [td.get_text(strip=True) for td in row.find_all("td")]
    # ["Alphonso Mango", "₹520", "₹450", "13%"]
```

Tables are easy: loop over rows (`<tr>`), then over cells (`<td>`).

---

## Step 4: Using and saving the data

Once the data is a Python list of dictionaries, you can do anything with it:

```python
best = max(fruits, key=lambda f: f["rating"])          # highest rated
in_stock = [f for f in fruits if f["in_stock"]]        # filter
```

And save it with the `csv` module:

```python
writer = csv.DictWriter(f, fieldnames=fruits[0].keys())
writer.writeheader()
writer.writerows(fruits)
```

---

## BeautifulSoup cheat sheet

| You want… | Code |
|-----------|------|
| First matching tag | `soup.find("h3", class_="name")` |
| All matching tags | `soup.find_all("article", class_="product")` |
| Tag by id | `soup.find("table", id="deals-table")` |
| Text inside a tag | `tag.get_text(strip=True)` |
| An attribute | `tag["href"]` or `tag.get("href")` |
| Page title | `soup.title.get_text()` |
| CSS selector (alternative) | `soup.select("article.product h3.name")` |

> `class_` has an underscore because `class` is a reserved word in Python.

---

## Exercises 🎯

Edit `shop.html`, re-run the script, and watch the output change.

1. **Add a fruit.** Copy one `<article class="product">` block, change the details, and run the scraper. Does it find 9 fruits?
2. **Scrape the stats.** Extract the three numbers in the stats strip (`<div class="stat">`).
3. **Filter by category.** Print only the `berry` fruits.
4. **Find the cheapest fruit** using `min()`.
5. **Grab the descriptions.** Add a `"description"` field from `<p class="description">`.
6. **Break it on purpose.** Rename `class="name"` to `class="title"` in the HTML. What error do you get? This is what happens when real websites change.

---

## Common problems

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'bs4'` | `pip install beautifulsoup4` |
| `OSError: Address already in use` | Something else is using port 8000. Change `PORT = 8000` to `8001` in the script. |
| `404 Not Found` | Run the script from **inside** the `local_scraping_demo` folder |
| `₹` shows as `â‚¹` | Make sure `response.encoding = "utf-8"` is set |
| `'NoneType' object has no attribute…` | A tag wasn't found. Check the tag name and class in the HTML. |

---

## Moving on to real websites

The same code works on real sites. Just change the URL and the tag names. When you do:

- Check the site's `robots.txt` (e.g. `https://example.com/robots.txt`) and Terms of Service.
- Add `time.sleep(1)` between requests so you don't overload the server.
- Use an official API if the site has one.
- Practise first on sites built for it: [quotes.toscrape.com](https://quotes.toscrape.com) and [books.toscrape.com](https://books.toscrape.com).
