from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# ==============================
# STYLE DEFINITIONS
# ==============================
STYLE_MAP = {
    "streetwear": ["oversized", "graphic", "baggy"],
    "minimalist": ["plain", "solid", "basic"],
    "casual": ["cotton", "regular", "comfortable"],
    "formal": ["shirt", "slim", "clean"],
    "vintage": ["floral", "retro", "classic"],
    "sporty": ["fit", "active", "stretch"],
    "funky": ["graphic", "bold", "colorful"],
    "anime": ["anime", "cartoon", "graphic"]
}

# precompute embeddings
style_embeddings = {
    style: model.encode(words)
    for style, words in STYLE_MAP.items()
}


# ==============================
# MAIN FUNCTION
# ==============================
def infer_styles(signal_counts):

    results = []

    for signal in signal_counts.keys():
        emb = model.encode([signal])

        best_style = None
        best_score = 0

        for style, emb_list in style_embeddings.items():
            score = cosine_similarity(emb, emb_list).max()

            if score > best_score:
                best_score = score
                best_style = style

        results.append(best_style)

    return results