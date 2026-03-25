import json
from collections import Counter

INPUT_FILE = "data/westside_detailed.json"


# ==============================
# BETTER CATEGORY NORMALIZATION
# ==============================
def normalize_category(name):
    name = name.lower()

    if "t-shirt" in name or "tshirt" in name:
        return "t-shirt"
    elif "shirt" in name:
        return "shirt"
    elif "trouser" in name or "pant" in name:
        return "bottomwear"
    elif "dress" in name:
        return "dress"
    elif "top" in name:
        return "top"
    elif "jacket" in name or "coat" in name:
        return "outerwear"
    elif "skirt" in name:
        return "skirt"
    else:
        return "other"


def saturation_engine():
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    category_list = []
    keyword_list = []

    for product in data:
        # 🔥 USE NORMALIZED CATEGORY
        category = normalize_category(product["name"])
        category_list.append(category)

        keyword_list.extend(product["keywords"])

    category_count = Counter(category_list)
    keyword_count = Counter(keyword_list)

    print("\n📊 CATEGORY DISTRIBUTION:\n")
    for cat, count in category_count.items():
        print(f"{cat}: {count}")

    print("\n🔥 KEYWORD DISTRIBUTION:\n")
    for key, count in keyword_count.items():
        print(f"{key}: {count}")

    # ==============================
    # SATURATION LOGIC
    # ==============================

    most_saturated = max(category_count, key=category_count.get)
    least_saturated = min(category_count, key=category_count.get)

    print("\n🚨 SATURATION INSIGHTS:\n")
    print(f"Most saturated category: {most_saturated}")
    print(f"Least saturated category: {least_saturated}")

    # ==============================
    # BETTER INSIGHT
    # ==============================

    insight = (
        f"High competition in '{most_saturated}' category. "
        f"Relatively less competition in '{least_saturated}', indicating a potential market opportunity."
    )

    print("\n🧠 FINAL INSIGHT:\n")
    print(insight)

    return {
        "category_distribution": dict(category_count),
        "keyword_distribution": dict(keyword_count),
        "most_saturated": most_saturated,
        "least_saturated": least_saturated,
        "insight": insight
    }


if __name__ == "__main__":
    saturation_engine()