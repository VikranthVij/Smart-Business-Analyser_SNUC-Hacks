from playwright.sync_api import sync_playwright
import json
import os
import time
import re

INPUT_FILE = "data/westside_products.json"
OUTPUT_FILE = "data/westside_detailed.json"


# ==============================
# CATEGORY DETECTION (IMPROVED)
# ==============================
def infer_category(name):
    name = name.lower()

    if "t-shirt" in name or "tee" in name:
        return "t-shirt"
    elif "shirt" in name:
        return "shirt"
    elif "jeans" in name:
        return "jeans"
    elif "dress" in name:
        return "dress"
    elif "jacket" in name:
        return "jacket"
    else:
        return "other"


# ==============================
# KEYWORD EXTRACTION (UPGRADED)
# ==============================
def extract_keywords(name):
    name = name.lower()
    keywords = []

    mapping = {
        "oversized": ["oversized", "loose", "baggy"],
        "graphic": ["graphic", "print", "printed", "logo"],
        "plain": ["solid", "plain", "basic"],
        "fit": ["slim", "regular", "relaxed"],
        "cotton": ["cotton"],
        "denim": ["denim"],
        "floral": ["floral"],
        "striped": ["stripe", "striped"],
        "polo": ["polo"],
        "crewneck": ["crew", "crewneck"],
    }

    for key, words in mapping.items():
        if any(w in name for w in words):
            keywords.append(key)

    return keywords


# ==============================
# PRICE EXTRACTION (FIXED)
# ==============================
def extract_price(page):
    try:
        page.wait_for_timeout(3000)

        texts = page.locator("text=₹").all()

        prices = []

        for t in texts:
            try:
                text = t.inner_text()

                match = re.search(r"₹\s?([\d,]+)", text)
                if match:
                    price = int(match.group(1).replace(",", ""))
                    prices.append(price)

            except:
                continue

        if not prices:
            return "N/A"

        return f"₹ {min(prices)}"

    except Exception as e:
        print("Price error:", e)
        return "N/A"


# ==============================
# DESCRIPTION EXTRACTION
# ==============================
def extract_description(page):
    try:
        page.wait_for_timeout(2000)

        paragraphs = page.locator("p").all()

        for p in paragraphs:
            text = p.inner_text().strip()

            if len(text) > 50:
                return text

        return "N/A"

    except:
        return "N/A"


# ==============================
# MAIN SCRAPER
# ==============================
def scrape_details():
    with open(INPUT_FILE, "r") as f:
        products = json.load(f)

    detailed = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for i, product in enumerate(products):
            try:
                print(f"\nProcessing {i+1}/{len(products)}")

                page.goto(product["link"], timeout=60000)

                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(4000)

                price = extract_price(page)
                description = extract_description(page)

                print("Price:", price)

                detailed.append({
                    "brand": "Westside",
                    "name": product["name"],
                    "price": price,
                    "category": infer_category(product["name"]),
                    "description": description,
                    "keywords": extract_keywords(product["name"]),
                    "link": product["link"]
                })

                time.sleep(1)

            except Exception as e:
                print("Error:", e)
                continue

        browser.close()

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(detailed, f, indent=4)

    print(f"\n✅ Detailed data saved ({len(detailed)} products)")


if __name__ == "__main__":
    scrape_details()