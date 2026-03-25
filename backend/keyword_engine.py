import json
import re
from collections import Counter

INPUT_FILE = "data/westside_detailed.json"


# ==============================
# CLEAN TEXT
# ==============================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


# ==============================
# EXTRACT KEYWORDS
# ==============================
def extract_keywords(name):
    words = clean_text(name).split()

    # remove common useless words
    stopwords = {
        "the", "and", "with", "for", "from",
        "high", "rise", "mid", "low",
        "nuon", "wardrobe", "gia", "lov",
        "westside"
    }

    keywords = [w for w in words if w not in stopwords and len(w) > 3]

    return keywords


# ==============================
# MAIN ENGINE
# ==============================
def keyword_engine():
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    all_keywords = []

    for product in data:
        name = product["name"]

        keywords = extract_keywords(name)

        all_keywords.extend(keywords)

    # count frequency
    keyword_counts = Counter(all_keywords)

    # top keywords
    top_keywords = keyword_counts.most_common(10)

    print("\n🔥 TOP KEYWORDS:\n")

    for word, count in top_keywords:
        print(f"{word}: {count}")

    # ==============================
    # INSIGHT GENERATION
    # ==============================

    insight = ""

    if top_keywords:
        dominant = top_keywords[0][0]

        insight = f"Most dominant trend is '{dominant}' indicating high competition in this category."

    print("\n🧠 INSIGHT:\n")
    print(insight)

    return {
        "top_keywords": dict(top_keywords),
        "insight": insight
    }


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    keyword_engine()