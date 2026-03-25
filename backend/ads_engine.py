import json

INPUT_FILE = "data/ads.json"


def ads_engine():

    try:
        with open(INPUT_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ ads.json not found")
        return {}

    print("\n📢 AD SIGNALS:\n")

    if not data:
        print("No ad signals found")
        return {}

    # sort signals
    sorted_data = dict(
        sorted(data.items(), key=lambda x: x[1], reverse=True)
    )

    # print top signals
    for k, v in list(sorted_data.items())[:10]:
        print(f"{k}: {v}")

    return sorted_data


if __name__ == "__main__":
    ads_engine()