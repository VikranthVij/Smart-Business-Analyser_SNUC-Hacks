from playwright.sync_api import sync_playwright
import json
import os
import time

INPUT_FILE = "data/westside_detailed.json"
OUTPUT_FILE = "data/reviews.json"


def generate_query(name):
    ignore = ["nuon", "wardrobe", "gia"]
    words = [w for w in name.lower().split() if w not in ignore]
    return " ".join(words[:4])


def scrape_reviews():
    with open(INPUT_FILE, "r") as f:
        products = json.load(f)

    all_reviews = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for product in products[:5]:  # limit for speed
            query = generate_query(product["name"])
            print(f"🔍 Searching: {query}")

            url = f"https://www.amazon.in/s?k={query}"
            page.goto(url, timeout=60000)
            page.wait_for_timeout(3000)

            try:
                page.click("h2 a")
                page.wait_for_timeout(5000)
            except:
                continue

            try:
                page.click("text=See all reviews")
                page.wait_for_timeout(3000)
            except:
                pass

            review_elements = page.query_selector_all("[data-hook=review-body]")

            for el in review_elements:
                try:
                    text = el.inner_text()
                    all_reviews.append({
                        "product": product["name"],
                        "text": text
                    })
                except:
                    continue

        browser.close()

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_reviews, f, indent=4)

    print(f"✅ Collected {len(all_reviews)} reviews")


if __name__ == "__main__":
    scrape_reviews()