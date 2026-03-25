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
SIMILARITY_THRESHOLD = 0.45   # 🔥 lowered for better recall
MIN_PATTERN_COUNT = 1         # 🔥 demo-safe
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
# SOURCE DETECTION (IMPORTANT)
# ==============================
def detect_source(text):

    # 🔥 simple heuristic
    if "amazon" in text:
        return "amazon"
    elif "google" in text:
        return "google"
    return "fallback"


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

    # store weighted results
    issue_scores = defaultdict(float)
    issue_counts = defaultdict(int)

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

        # 🔥 weighted aggregation
        issue_scores[issue] += score * weight
        issue_counts[issue] += weight

    # ==============================
    # FINAL SCORING
    # ==============================
    final_issues = {}

    for issue in issue_counts:

        count = issue_counts[issue]

        if count < MIN_PATTERN_COUNT:
            continue

        avg_conf = issue_scores[issue] / count

        final_issues[issue] = {
            "count": count,
            "confidence": round(avg_conf, 2)
        }

    # ==============================
    # OUTPUT
    # ==============================
    print("\n🚨 VALIDATED CUSTOMER ISSUES:\n")

    if not final_issues:
        print("No strong patterns detected")
    else:
        for issue, data in final_issues.items():
            print(f"{issue}: {data['count']} (confidence: {data['confidence']})")

    return final_issues


if __name__ == "__main__":
    review_engine()