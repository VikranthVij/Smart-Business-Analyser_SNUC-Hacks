from playwright.sync_api import sync_playwright
import json
import os
import time

URL = "https://www.westside.com/collections/men-t-shirts"


def clean_link(link):
    if not link:
        return None

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

        # 🔥 STRONG SCROLL (LOAD MORE PRODUCTS)
        prev_count = 0

        for i in range(12):  # increased scroll depth
            page.mouse.wheel(0, 6000)
            page.wait_for_timeout(2000)

            products = page.query_selector_all("a[href*='/products/']")
            curr_count = len(products)

            print(f"Scroll {i+1}: Found {curr_count} products")

            # stop if no new products loaded
            if curr_count == prev_count:
                break

            prev_count = curr_count

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

                # better filtering
                if not name or len(name.split()) < 2:
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

        print(f"\n✅ Scraped {len(data)} products")


if __name__ == "__main__":
    scrape()