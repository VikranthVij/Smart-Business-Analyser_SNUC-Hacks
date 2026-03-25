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
    # SAFE EXTRACTION
    # ==============================

    trend_counts = trend_data.get("trend_counts", {}) if trend_data else {}

    # get top trend
    top_trend = max(trend_counts, key=trend_counts.get) if trend_counts else None
    top_trend_score = trend_counts.get(top_trend, 0) if top_trend else 0

    # get top issue
    top_issue = max(review_data, key=review_data.get) if review_data else None
    top_issue_score = review_data.get(top_issue, 0) if top_issue else 0

    # get top ad keyword
    top_ad = max(ads_data, key=ads_data.get) if ads_data else None
    top_ad_score = ads_data.get(top_ad, 0) if top_ad else 0

    # ==============================
    # CROSS-SIGNAL ANALYSIS
    # ==============================

    trend_in_ads = top_trend in ads_data if top_trend and ads_data else False

    # ==============================
    # PRINT CORE INSIGHTS
    # ==============================

    print(f"🔥 Market Trend: {top_trend} (score: {top_trend_score})")
    print(f"⚠️ Customer Issue: {top_issue} (mentions: {top_issue_score})")
    print(f"📢 Competitor Focus: {top_ad} (frequency: {top_ad_score})")

    print("\n💡 RECOMMENDATION:\n")

    # ==============================
    # INTELLIGENT DECISION LOGIC
    # ==============================

    if top_trend and top_issue:

        if trend_in_ads:
            print(
                f"'{top_trend}' is heavily promoted and trending, but customers report '{top_issue}' issues.\n"
                f"👉 STRATEGY: Build superior '{top_trend}' products by fixing '{top_issue}'.\n"
                f"👉 This is a HIGH-IMPACT opportunity."
            )
        else:
            print(
                f"'{top_trend}' is trending but not heavily promoted yet.\n"
                f"👉 STRATEGY: Enter early and solve '{top_issue}' issues.\n"
                f"👉 This is a FIRST-MOVER opportunity."
            )

    elif top_trend:
        print(
            f"'{top_trend}' is trending with no major issues detected.\n"
            f"👉 STRATEGY: Compete on branding, pricing, or differentiation."
        )

    elif top_issue:
        print(
            f"Customers frequently complain about '{top_issue}'.\n"
            f"👉 STRATEGY: Solve this issue across product lines for competitive advantage."
        )

    else:
        print("No strong insights detected.")

    print("\n📊 SYSTEM CONFIDENCE:\n")

    print(f"Trend Strength: {top_trend_score}")
    print(f"Issue Strength: {top_issue_score}")
    print(f"Ad Strength: {top_ad_score}")

    print("\n✅ Analysis Complete.\n")


if __name__ == "__main__":
    intelligence_engine()