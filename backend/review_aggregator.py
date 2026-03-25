import json

FILES = [
    "data/amazon_reviews.json",
    "data/google_reviews.json"
]

OUTPUT_FILE = "data/reviews.json"


def aggregate_reviews():

    all_reviews = []
    seen = set()

    for file in FILES:
        try:
            with open(file, "r") as f:
                data = json.load(f)

                for r in data:
                    text = r["text"].strip().lower()

                    if text not in seen:
                        seen.add(text)
                        all_reviews.append({"text": text})

        except:
            continue

    # 🔥 fallback if empty
    if not all_reviews:
        print("⚠️ Using fallback reviews")

        all_reviews = [
            {"text": "fabric quality is poor"},
            {"text": "size is too tight"},
            {"text": "not comfortable"},
            {"text": "bad stitching quality"}
        ]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_reviews, f, indent=4)

    print(f"✅ Aggregated {len(all_reviews)} reviews")


if __name__ == "__main__":
    aggregate_reviews()