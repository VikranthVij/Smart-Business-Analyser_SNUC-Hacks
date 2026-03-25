import time
import random
import json
import re
import os
import pandas as pd
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
from groq import Groq

# ---------------- INIT ----------------

app = FastAPI()

# ✅ FIXED: CORS must be added to the instance that is actually running
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use environment variable for security, or fallback to the provided key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

pytrends = TrendReq(
    hl='en-IN',
    tz=330,
    requests_args={"headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}}
)

# ---------------- MODELS ----------------

class KeywordRequest(BaseModel):
    keywords: List[str]

class TrendsResponse(BaseModel):
    trends: List[str]

# ---------------- GOOGLE TRENDS ----------------

def safe_get_related(keyword, retries=2):
    for _ in range(retries):
        try:
            # Shortened timeframe for faster response
            pytrends.build_payload([keyword], timeframe='today 3-m', geo='IN')
            time.sleep(random.uniform(1, 2)) # Reduced wait time slightly
            return pytrends.related_queries()
        except TooManyRequestsError:
            time.sleep(5)
        except Exception as e:
            print(f"Error fetching {keyword}: {e}")
            break
    return None

# ---------------- FALLBACK ----------------

def fallback_queries(keyword):
    return [
        f"{keyword} summer outfits india",
        f"{keyword} streetwear india",
        f"{keyword} oversized trends",
    ]

# ---------------- GROQ FILTER ----------------

def filter_clothing_trends(queries):
    prompt = f"""
Return ONLY a valid JSON array of clothing or fashion-related strings.
Exclude anything unrelated to apparel.

Rules:
- No explanation
- No markdown
- Use double quotes

Queries:
{queries}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        result = response.choices[0].message.content.strip()

        # Clean markdown if present
        result = re.sub(r"```json|```", "", result).strip()
        match = re.search(r"\[.*\]", result, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return []
    except Exception as e:
        print(f"Groq Error: {e}")
        # Return raw queries if AI filtering fails
        return queries[:10]

# ---------------- MAIN LOGIC ----------------

def process_keywords(keywords):
    all_queries = []

    for keyword in keywords:
        related = safe_get_related(keyword)

        if not related or not related.get(keyword):
            all_queries.extend(fallback_queries(keyword))
            continue

        keyword_data = related.get(keyword)
        for t in ["top", "rising"]:
            df = keyword_data.get(t)
            if df is not None and not df.empty:
                all_queries.extend(df["query"].tolist())

    # Deduplicate and clean
    all_queries = list(set(q.lower().strip() for q in all_queries if isinstance(q, str)))

    if not all_queries:
        return []

    filtered = filter_clothing_trends(all_queries)
    return sorted(filtered, key=len)[:10]

# ---------------- API ROUTES ----------------

@app.get("/")
def home():
    return {"status": "online", "message": "Fashion Trends API is running 🚀"}

@app.post("/trends", response_model=TrendsResponse)
async def get_trends(request: KeywordRequest):
    results = process_keywords(request.keywords)
    return {"trends": results}