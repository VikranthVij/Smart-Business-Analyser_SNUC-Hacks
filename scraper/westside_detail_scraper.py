from playwright.sync_api import sync_playwright
import json
import os
import time

INPUT_FILE = "data/westside_products.json"
OUTPUT_FILE = "data/westside_detailed.json"


def infer_category(name):
    name = name.lower()

    if "t-shirt" in name:
        return "t-shirt"
    elif "shirt" in name:
        return "shirt"
    elif "jeans" in name:
        return "jeans"
    else:
        return "other"


def extract_keywords(name):
    name = name.lower()
    keywords = []

    if "oversized" in name:
        keywords.append("oversized")

    if any(x in name for x in ["graphic", "print", "logo"]):
        keywords.append("graphic")

    return keywords


def extract_price(page):
    try:
        page.wait_for_timeout(2000)

        prices = []

        elements = page.locator("text=₹").all()

        for el in elements:
            try:
                text = el.inner_text().strip()

                if "₹" in text:
                    # clean text → remove ₹ and commas
                    clean = text.replace("₹", "").replace(",", "").strip()

                    # extract number
                    import re
                    match = re.search(r"\d+", clean)

                    if match:
                        prices.append(int(match.group()))

            except:
                continue

        if not prices:
            return "N/A"

        # 🔥 IMPORTANT LOGIC
        # take MIN price (discounted price)
        final_price = min(prices)

        return f"₹ {final_price}"

    except Exception as e:
        print("Price error:", e)
        return "N/A"


def extract_description(page):
    try:
        elements = page.locator("p").all()

        for el in elements:
            text = el.inner_text().strip()

            if len(text) > 40:
                return text

        return "N/A"

    except:
        return "N/A"


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
                page.wait_for_timeout(3000)

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