from rules.rule_engine import apply_rules
from engine.strategy_engine import generate_strategy
from guardrails.guardrails import apply_guardrails
from utils.formatter import clean_output
from analysis.trend_detector import detect_trends
from analysis.whitespace_detector import detect_whitespace
import os

os.environ["GROQ_API_KEY"] = ""
# SAMPLE SCRAPED DATA (simulate for now)
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

# Step 3: Build context
context = {
    "trends": trends,
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