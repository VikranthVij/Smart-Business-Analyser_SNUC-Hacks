import json
import os
from collections import Counter

INPUT_FILE = "data/westside_detailed.json"
OUTPUT_FILE = "data/ads.json"

# ==============================
# FILTER CONFIG
# ==============================

# ❌ remove useless/generic signals
IGNORE = ["color", "material", "other"]

# ❌ remove category-only signals (not trends)
REMOVE = ["t-shirt", "shirt", "dress", "jeans"]

# ✅ high-value trend signals
PRIORITY = [
    "oversized", "graphic", "plain",
    "fit", "cotton", "denim",
    "floral", "striped", "polo",
    "crewneck"
]

# 🔥 minimum frequency to be considered meaningful
MIN_THRESHOLD = 2


# ==============================
# MAIN FUNCTION
# ==============================
def scrape_ads():

    with open(INPUT_FILE, "r") as f:
        products = json.load(f)

    all_signals = []

    for p in products:
        keywords = p.get("keywords", [])
        category = p.get("category", "")

        # normalize keywords
        keywords = [k.lower().strip() for k in keywords if k]

        # add keyword signals
        for k in keywords:
            if k not in IGNORE:
                all_signals.append(k)

        # add category (only if meaningful)
        if category and category not in IGNORE:
            all_signals.append(category.lower())

    # ==============================
    # COUNT SIGNALS
    # ==============================
    counts = Counter(all_signals)

    # ==============================
    # FILTER SIGNALS
    # ==============================
    filtered = {}

    for k, v in counts.items():

        # remove weak signals
        if v < MIN_THRESHOLD:
            continue

        # remove generic categories
        if k in REMOVE:
            continue

        # keep only priority or strong signals
        if k in PRIORITY or v >= 3:
            filtered[k] = v

    # ==============================
    # SORT
    # ==============================
    filtered = dict(
        sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    )

    # ==============================
    # SAVE
    # ==============================
    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(filtered, f, indent=4)

    # ==============================
    # OUTPUT
    # ==============================
    print("\n📢 FINAL AD SIGNALS:\n")

    if not filtered:
        print("No strong signals found")
    else:
        for k, v in filtered.items():
            print(f"{k}: {v}")

    return filtered


if __name__ == "__main__":
    scrape_ads()