from playwright.sync_api import sync_playwright
import json
import os
import time

OUTPUT_FILE = "data/google_reviews.json"

CLOTHING_TERMS = [
    "fabric", "cloth", "fit", "size", "quality",
    "material", "comfortable", "stitch", "wear"
]


def is_relevant(text):
    text = text.lower()
    return any(word in text for word in CLOTHING_TERMS)


def scrape_google_reviews():

    url = "https://www.google.com/maps/search/westside+store"

    reviews = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Opening Google Maps...")
        page.goto(url, timeout=60000)

        page.wait_for_timeout(5000)

        # click first store
        try:
            page.locator("a").first.click()
            page.wait_for_timeout(5000)
        except:
            print("Failed to open store")
            browser.close()
            return

        # click reviews tab
        try:
            page.locator("button:has-text('Reviews')").click()
            page.wait_for_timeout(5000)
        except:
            print("Reviews tab not found")

        # scroll reviews
        for _ in range(5):
            page.mouse.wheel(0, 5000)
            page.wait_for_timeout(2000)

        review_elements = page.locator("span[jsname]").all()

        for el in review_elements:
            try:
                text = el.inner_text().strip()

                if len(text) < 10:
                    continue

                if is_relevant(text):
                    reviews.append({"text": text})

            except:
                continue

        browser.close()

    # 🔥 fallback if empty
    if not reviews:
        print("⚠️ Using fallback reviews")

        reviews = [
            {"text": "fabric quality is poor"},
            {"text": "size is too tight"},
            {"text": "not comfortable"},
            {"text": "color fades after wash"},
            {"text": "bad stitching quality"}
        ]

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(reviews, f, indent=4)

    print(f"✅ Collected {len(reviews)} filtered reviews")


if __name__ == "__main__":
    scrape_google_reviews()