import json
from collections import Counter

INPUT_FILE = "data/ads.json"


def ads_engine():
    with open(INPUT_FILE, "r") as f:
        ads = json.load(f)

    keywords = []

    for ad in ads:
        text = ad["ad_text"].lower().split()

        for word in text:
            if len(word) > 4:
                keywords.append(word)

    keyword_count = Counter(keywords)

    print("\n📢 AD TRENDS:\n")

    for k, v in keyword_count.most_common(10):
        print(f"{k}: {v}")

    return dict(keyword_count)


if __name__ == "__main__":
    ads_engine()