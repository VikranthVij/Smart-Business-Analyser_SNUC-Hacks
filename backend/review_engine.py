import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

INPUT_FILE = "data/reviews.json"

# ==============================
# LOAD MODEL
# ==============================
model = SentenceTransformer('all-MiniLM-L6-v2')

# ==============================
# ISSUE DEFINITIONS
# ==============================
ISSUES = {
    "size": [
        "too small", "too big", "tight", "loose",
        "fit issue", "size mismatch"
    ],
    "quality": [
        "poor quality", "cheap fabric", "bad stitching",
        "low durability", "torn", "weak material"
    ],
    "comfort": [
        "not comfortable", "itchy", "rough",
        "uncomfortable", "hard to wear"
    ],
    "color": [
        "faded", "color mismatch", "color bleed",
        "color fades", "dull color"
    ]
}

issue_embeddings = {
    k: model.encode(v)
    for k, v in ISSUES.items()
}

# ==============================
# CONFIG
# ==============================
SIMILARITY_THRESHOLD = 0.45
MIN_PATTERN_COUNT = 1
MIN_LENGTH = 5

# ==============================
# SOURCE WEIGHTS
# ==============================
SOURCE_WEIGHTS = {
    "amazon": 2,
    "google": 1,
    "fallback": 1
}

# ==============================
# VALIDATION
# ==============================
def is_valid_review(text, seen):

    text = text.lower().strip()

    if len(text.split()) < MIN_LENGTH:
        return False

    if text in seen:
        return False

    irrelevant = [
        "delivery", "packing", "refund",
        "billing", "staff", "late"
    ]
    if any(w in text for w in irrelevant):
        return False

    return True


# ==============================
# CLASSIFICATION
# ==============================
def classify_review(text):

    emb = model.encode([text])

    best_issue = None
    best_score = 0

    for issue, emb_list in issue_embeddings.items():
        score = cosine_similarity(emb, emb_list).max()

        if score > best_score:
            best_score = score
            best_issue = issue

    if best_score < SIMILARITY_THRESHOLD:
        return None, 0

    return best_issue, best_score


# ==============================
# INTERPRETATION HELPERS
# ==============================
def confidence_label(score):
    if score > 0.75:
        return "HIGH"
    elif score > 0.6:
        return "MEDIUM"
    return "LOW"


def generate_reason(issue, count):
    reasons = {
        "quality": "Multiple reviews highlight issues with fabric durability and stitching quality.",
        "size": "Customers report inconsistent sizing and poor fit accuracy.",
        "comfort": "Users mention discomfort, rough fabric, or poor wearability.",
        "color": "Complaints about color fading or mismatch are observed."
    }
    return reasons.get(issue, "Pattern detected from multiple customer complaints.")


def generate_suggestion(issue):
    suggestions = {
        "quality": "Improve fabric quality and stitching to enhance durability.",
        "size": "Standardize sizing and improve fit consistency.",
        "comfort": "Use softer materials and improve wearability.",
        "color": "Enhance dye quality to prevent fading issues."
    }
    return suggestions.get(issue, "Improve product based on customer feedback.")


# ==============================
# MAIN ENGINE
# ==============================
def review_engine():

    try:
        with open(INPUT_FILE, "r") as f:
            reviews = json.load(f)
    except:
        print("❌ No reviews file found")
        return {}

    seen = set()

    issue_scores = defaultdict(float)
    issue_counts = defaultdict(int)
    issue_samples = defaultdict(list)

    for r in reviews:
        text = r.get("text", "").strip()

        if not text:
            continue

        if not is_valid_review(text, seen):
            continue

        seen.add(text)

        issue, score = classify_review(text)

        if not issue:
            continue

        source = r.get("source", "fallback")
        weight = SOURCE_WEIGHTS.get(source, 1)

        issue_scores[issue] += score * weight
        issue_counts[issue] += weight

        # store sample reviews (max 3)
        if len(issue_samples[issue]) < 3:
            issue_samples[issue].append(text)

    print("\n🚨 DETAILED CUSTOMER ISSUE ANALYSIS:\n")

    if not issue_counts:
        print("No strong patterns detected")
        return {}

    for issue in issue_counts:

        count = issue_counts[issue]

        if count < MIN_PATTERN_COUNT:
            continue

        avg_conf = issue_scores[issue] / count
        label = confidence_label(avg_conf)

        print(f"🔴 ISSUE: {issue.upper()}\n")
        print(f"Mentions: {count}")
        print(f"Confidence: {round(avg_conf, 2)} ({label})\n")

        print("Reason:")
        print(generate_reason(issue, count), "\n")

        print("Sample Evidence:")
        for sample in issue_samples[issue]:
            print(f"- {sample}")
        print()

        print("Interpretation:")
        print(f"This issue appears consistently across reviews, indicating a reliable customer concern.\n")

        print("Business Suggestion:")
        print(generate_suggestion(issue))
        print("\n" + "="*50 + "\n")

    return issue_counts


if __name__ == "__main__":
    review_engine()