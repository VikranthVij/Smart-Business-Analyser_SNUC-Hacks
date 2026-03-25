import json
import os

OUTPUT_FILE = "data/amazon_reviews.json"

def scrape_amazon_reviews():

    print("🔍 Simulating Amazon review scraping...")

    # 🔥 Simulated but realistic (hackathon safe)
    reviews = [
        {"text": "fabric quality is very poor"},
        {"text": "size runs too small"},
        {"text": "bad stitching and cheap material"},
        {"text": "not comfortable to wear"},
        {"text": "color fades quickly"}
    ]

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(reviews, f, indent=4)

    print(f"✅ Amazon reviews collected: {len(reviews)}")


if __name__ == "__main__":
    scrape_amazon_reviews()