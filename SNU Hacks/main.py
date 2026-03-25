from rules.rule_engine import apply_rules
from engine.strategy_engine import generate_strategy
from guardrails.guardrails import apply_guardrails
from utils.formatter import clean_output
from analysis.trend_detector import detect_trends
from analysis.whitespace_detector import detect_whitespace
import os
from rag.retriever import retrieve_context, store_data
from memory.user_memory import get_user_profile, update_user_profile
from memory.smart_store import store_interaction, store_market, store_strategy
from memory.smart_store import store_strategy, store_market, store_interaction

os.environ["GROQ_API_KEY"] = "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"
# SAMPLE SCRAPED DATA (simulate for now)
user_id = "nittin"
profile = get_user_profile(user_id)
company_data = [
    "AI powered productivity for enterprise teams",
    "automation and AI workflows for businesses",
    "enterprise collaboration with smart automation"
]

# Step 1: Detect trends
trends = detect_trends(company_data)

# Step 2: Detect whitespace
segments = ["enterprise", "teams"]
whitespace = detect_whitespace(segments)

user_query = "AI business strategy for enterprise tools"  # or your actual input

rag_data = retrieve_context(user_query)
print("RAG DATA:", rag_data)
# Step 3: Build context
context = {
    "rag_strategy": rag_data["strategy"],
    "rag_market": rag_data["market"],
    "rag_interaction": rag_data["interaction"],   # 🔥 ADD THIS LINE
    "trends": trends,
    "user_profile": profile, 
    "overused": ["productivity", "all-in-one"],
    "whitespace": whitespace,
    "actions": [
        "Slack added AI features",
        "Notion updated pricing"
    ]
}
# Step 4: Apply rules
rules_output = apply_rules(context)

# Step 5: Tone selection
tone = "professional and strategic"

# Step 6: Generate strategy
response = generate_strategy(context, rules_output, tone)

# Step 7: Guardrails
valid, result = apply_guardrails(response)

if not valid:
    print("Guardrail Triggered:", result)
else:
    final_output = clean_output(result)
    print("\nFINAL OUTPUT:\n")
    print(final_output)
    store_data(user_query)
    
    
    store_interaction(user_id, user_query)

    
    store_market(user_id, trends, whitespace)

    
    store_strategy(user_id, user_query, final_output)
    update_user_profile(user_id, {
        "last_query": user_query
    })