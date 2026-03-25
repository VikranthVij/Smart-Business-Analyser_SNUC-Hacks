import os
from scraper.amazon_review_scraper import scrape_amazon_reviews
from scraper.google_reviews_scraper import scrape_google_reviews
from backend.review_aggregator import aggregate_reviews

print("🚀 Starting Full Pipeline...\n")

# Scrapers
os.system("python3 scraper/westside_scraper.py")
os.system("python3 scraper/westside_detail_scraper.py")
os.system("python3 scraper/review_scraper.py")
os.system("python3 scraper/ads_scraper.py")

# Engines
os.system("python3 backend/trend_engine.py")
scrape_amazon_reviews()
scrape_google_reviews()
aggregate_reviews()
os.system("python3 backend/review_engine.py")
os.system("python3 backend/ads_engine.py")
os.system("python3 backend/intelligence_engine.py")

print("\n✅ Pipeline Completed")