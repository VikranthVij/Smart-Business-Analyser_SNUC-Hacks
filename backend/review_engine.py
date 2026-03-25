import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

INPUT_FILE = "data/reviews.json"

# ==============================
# LOAD MODEL (only once)
# ==============================
model = SentenceTransformer('all-MiniLM-L6-v2')

# ==============================
# ISSUE DEFINITIONS
# ==============================
ISSUES = {
    "size": ["too small", "too big", "tight", "loose", "fit issue"],
    "quality": ["poor quality", "cheap fabric", "bad stitching", "low durability"],
    "comfort": ["not comfortable", "itchy", "rough", "uncomfortable"],
    "color": ["faded", "color mismatch", "color bleed"]
}

# Convert issues to embeddings
issue_embeddings = {
    key: model.encode(values)
    for key, values in ISSUES.items()
}

# ==============================
# CONFIG
# ==============================
SIMILARITY_THRESHOLD = 0.55
MIN_PATTERN_COUNT = 2


# ==============================
# CLASSIFY REVIEW
# ==============================
def classify_review(text):
    review_emb = model.encode([text])

    best_issue = None
    best_score = 0

    for issue, emb_list in issue_embeddings.items():
        sim = cosine_similarity(review_emb, emb_list).max()

        if sim > best_score:
            best_score = sim
            best_issue = issue

    # Reject if not confident
    if best_score < SIMILARITY_THRESHOLD:
        return None

    return best_issue


# ==============================
# FILTER REVIEWS
# ==============================
def is_valid_review(text, seen):

    # Length filter
    if len(text.split()) < 5:
        return False

    # Duplicate filter
    if text in seen:
        return False

    # Irrelevant filter
    irrelevant_words = ["delivery", "packing", "late", "refund"]
    if any(word in text.lower() for word in irrelevant_words):
        return False

    return True


# ==============================
# MAIN ENGINE
# ==============================
def review_engine():

    with open(INPUT_FILE, "r") as f:
        reviews = json.load(f)

    seen = set()
    classified_issues = []

    for r in reviews:
        text = r["text"].strip()

        if not is_valid_review(text, seen):
            continue

        seen.add(text)

        issue = classify_review(text)

        if issue:
            classified_issues.append(issue)

    # Count issues
    counts = Counter(classified_issues)

    # Apply pattern validation (IMPORTANT)
    filtered_counts = {
        issue: count for issue, count in counts.items()
        if count >= MIN_PATTERN_COUNT
    }

    print("\n🚨 VALIDATED CUSTOMER ISSUES:\n")

    if not filtered_counts:
        print("No strong patterns detected")
    else:
        for k, v in filtered_counts.items():
            print(f"{k}: {v}")

    return filtered_counts


if __name__ == "__main__":
    review_engine()