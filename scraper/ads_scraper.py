from playwright.sync_api import sync_playwright
import json
import os

OUTPUT_FILE = "data/ads.json"


def scrape_ads():
    ads = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://www.facebook.com/ads/library")
        page.wait_for_timeout(5000)

        try:
            page.fill("input", "Westside")
            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)
        except:
            print("Search failed")

        elements = page.query_selector_all("div")

        for el in elements[:50]:
            try:
                text = el.inner_text()
                if len(text) > 50:
                    ads.append({"ad_text": text})
            except:
                continue

        browser.close()

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(ads, f, indent=4)

    print(f"✅ Collected {len(ads)} ads")


if __name__ == "__main__":
    scrape_ads()