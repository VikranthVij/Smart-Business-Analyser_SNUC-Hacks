from playwright.sync_api import sync_playwright
import json
import os

URL = "https://www.westside.com/collections/men-t-shirts"


def clean_link(link):
    if not link:
        return None

    # FIX malformed links
    if link.startswith("https//"):
        link = "https://" + link.split("https//")[1]

    if link.startswith("http"):
        return link

    return "https://www.westside.com" + link


def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Opening Westside...")
        page.goto(URL, timeout=60000)

        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(4000)

        # Scroll
        for _ in range(5):
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(2000)

        products = page.query_selector_all("a[href*='/products/']")

        data = []
        seen = set()

        for product in products:
            try:
                raw_link = product.get_attribute("href")
                link = clean_link(raw_link)

                if not link or link in seen:
                    continue

                seen.add(link)

                name = product.inner_text().strip()

                if len(name) < 5:
                    continue

                data.append({
                    "brand": "Westside",
                    "name": name,
                    "link": link
                })

            except:
                continue

        browser.close()

        os.makedirs("data", exist_ok=True)

        with open("data/westside_products.json", "w") as f:
            json.dump(data, f, indent=4)

        print(f"✅ Scraped {len(data)} products")


if __name__ == "__main__":
    scrape()