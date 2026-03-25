import os
from scraper.amazon_review_scraper import scrape_amazon_reviews
from scraper.google_reviews_scraper import scrape_google_reviews
from backend.review_aggregator import aggregate_reviews

import sys

print("🚀 Starting Full Pipeline...\n")

# Scrapers
os.system(f"{sys.executable} scraper/westside_scraper.py")
os.system(f"{sys.executable} scraper/westside_detail_scraper.py")
os.system(f"{sys.executable} scraper/review_scraper.py")
os.system(f"{sys.executable} scraper/ads_scraper.py")

# Engines
os.system(f"{sys.executable} backend/trend_engine.py")
scrape_amazon_reviews()
scrape_google_reviews()
aggregate_reviews()
os.system(f"{sys.executable} backend/review_engine.py")
os.system(f"{sys.executable} backend/ads_engine.py")
os.system(f"{sys.executable} backend/intelligence_engine.py")

print("\n✅ Pipeline Completed")