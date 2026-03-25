import json
from collections import Counter

INPUT_FILE = "data/reviews.json"


NEGATIVE_KEYWORDS = [
    "bad", "poor", "worst", "small", "tight",
    "loose", "quality", "cheap", "fade",
    "shrink", "tear", "defect"
]


def review_engine():
    with open(INPUT_FILE, "r") as f:
        reviews = json.load(f)

    issues = []

    for r in reviews:
        text = r["text"].lower()
        rating = r["rating"]

        # focus only negative reviews
        if rating <= 2:
            for word in NEGATIVE_KEYWORDS:
                if word in text:
                    issues.append(word)

    issue_count = Counter(issues)

    print("\n🚨 TOP CUSTOMER COMPLAINTS:\n")

    for issue, count in issue_count.items():
        print(f"{issue}: {count}")

    return dict(issue_count)


if __name__ == "__main__":
    review_engine()