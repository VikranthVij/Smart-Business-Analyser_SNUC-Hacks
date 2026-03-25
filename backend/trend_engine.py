import json
from collections import Counter

INPUT_FILE = "data/westside_detailed.json"


# ==============================
# TREND DICTIONARY
# ==============================

TREND_KEYWORDS = {
    "style": [
        "floral", "printed", "print", "velvet",
        "faux", "leather", "denim", "ribbed",
        "knit", "textured", "embroidered"
    ],
    "fit": [
        "oversized", "slim", "regular",
        "high-rise", "mid-rise", "low-rise"
    ],
    "theme": [
        "anime", "marvel", "dc", "graphic"
    ],
    "color": [
        "black", "white", "brown", "blue",
        "green", "pink", "multicolour"
    ]
}


# ==============================
# EXTRACT TRENDS
# ==============================

def extract_trends(name):
    name = name.lower()
    trends = []

    for category in TREND_KEYWORDS.values():
        for keyword in category:
            if keyword in name:
                trends.append(keyword)

    return trends


# ==============================
# SATURATION LOGIC
# ==============================

def get_saturation_level(count):
    if count >= 5:
        return "high"
    elif count >= 3:
        return "medium"
    else:
        return "low"


# ==============================
# MAIN ENGINE
# ==============================

def trend_engine():
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    trend_list = []

    for product in data:
        name = product["name"]
        trends = extract_trends(name)
        trend_list.extend(trends)

    trend_counts = Counter(trend_list)

    print("\n🔥 TREND DISTRIBUTION:\n")
    for trend, count in trend_counts.items():
        print(f"{trend}: {count}")

    # ==============================
    # SATURATION ANALYSIS
    # ==============================

    trend_saturation = {}

    for trend, count in trend_counts.items():
        trend_saturation[trend] = get_saturation_level(count)

    print("\n📊 TREND SATURATION:\n")
    for trend, level in trend_saturation.items():
        print(f"{trend}: {level}")

    # ==============================
    # OPPORTUNITY DETECTION
    # ==============================

    low_trends = [t for t, lvl in trend_saturation.items() if lvl == "low"]
    high_trends = [t for t, lvl in trend_saturation.items() if lvl == "high"]

    print("\n🚨 OPPORTUNITIES:\n")

    if low_trends:
        print(f"Low competition trends: {', '.join(low_trends)}")

    if high_trends:
        print(f"Highly saturated trends: {', '.join(high_trends)}")

    # ==============================
    # FINAL INSIGHT
    # ==============================

    insight = ""

    if low_trends:
        insight = f"Opportunity detected in {low_trends[0]} category with low competition."
    elif high_trends:
        insight = f"{high_trends[0]} is highly saturated. Avoid entering this segment."

    print("\n🧠 FINAL INSIGHT:\n")
    print(insight)

    return {
        "trend_counts": dict(trend_counts),
        "trend_saturation": trend_saturation,
        "low_trends": low_trends,
        "high_trends": high_trends,
        "insight": insight
    }


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    trend_engine()