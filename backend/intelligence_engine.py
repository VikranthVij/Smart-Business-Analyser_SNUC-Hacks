from trend_engine import trend_engine
from review_engine import review_engine
from ads_engine import ads_engine


def intelligence_engine():

    print("\n🔍 RUNNING FULL INTELLIGENCE SYSTEM...\n")

    trend_data = trend_engine()
    review_data = review_engine()
    ads_data = ads_engine()

    print("\n🧠 FINAL BUSINESS INSIGHTS:\n")

    # ==============================
    # LOGIC
    # ==============================

    # get top trend
    if trend_data["trend_counts"]:
        top_trend = max(trend_data["trend_counts"], key=trend_data["trend_counts"].get)
    else:
        top_trend = None

    # get major issue
    if review_data:
        top_issue = max(review_data, key=review_data.get)
    else:
        top_issue = None

    # get top ad keyword
    if ads_data:
        top_ad = max(ads_data, key=ads_data.get)
    else:
        top_ad = None

    # ==============================
    # FINAL INSIGHT
    # ==============================

    print(f"🔥 Market Trend: {top_trend}")
    print(f"⚠️ Customer Issue: {top_issue}")
    print(f"📢 Competitor Focus: {top_ad}")

    print("\n💡 RECOMMENDATION:\n")

    if top_trend and top_issue:
        print(
            f"The '{top_trend}' segment is trending but has issues related to '{top_issue}'. "
            f"Opportunity to improve and capture market."
        )
    elif top_trend:
        print(f"Focus on '{top_trend}' as it is trending.")
    else:
        print("No strong insights detected.")


if __name__ == "__main__":
    intelligence_engine()