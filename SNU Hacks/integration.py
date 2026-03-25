import os
import sys

# Add SNU Hacks path so imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from rules.rule_engine import apply_rules
from engine.strategy_engine import generate_strategy
from guardrails.guardrails import apply_guardrails
from utils.formatter import clean_output
from rag.retriever import retrieve_context, store_data
from memory.user_memory import get_user_profile, update_user_profile
from memory.smart_store import store_interaction, store_market, store_strategy

def run_langchain_analysis(top_trend, top_issue, top_ad, company_data=None):
    os.environ["GROQ_API_KEY"] = "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"
    user_id = "default_user"
    profile = get_user_profile(user_id)
    
    if not company_data:
        company_data = ["Smart Business Analyser"]

    # Format the insights gathered from intelligence engine
    trends = [top_trend] if top_trend else []
    whitespace = [top_issue] if top_issue else [] # Treated as whitespace/issues to solve
    
    # Create the user query context correctly
    user_query = f"How to address {top_issue} while capitalizing on {top_trend} given competitors focus on {top_ad}?"

    rag_data = retrieve_context(user_query)
    
    # Combine rag data to context expected by strategy_engine
    rag_context = rag_data.get("strategy", []) + rag_data.get("market", []) + rag_data.get("interaction", [])
    
    context = {
        "rag_context": rag_context,
        "trends": trends,
        "user_profile": profile, 
        "overused": [top_ad] if top_ad else [],
        "whitespace": whitespace,
        "actions": []
    }

    rules_output = apply_rules(context)
    tone = "professional, strategic, and data-driven"
    
    response = generate_strategy(context, rules_output, tone)
    
    valid, result = apply_guardrails(response.content if hasattr(response, 'content') else response)
    
    if not valid:
        return f"Guardrail Triggered: {result}"
    
    final_output = clean_output(result)
    
    # Store history for memory
    store_data(user_query)
    store_interaction(user_id, user_query)
        
    try:
        # Avoid issues if these fail
        store_market(user_id, trends, whitespace)
    except Exception:
        pass

    try:
        store_strategy(user_id, user_query, final_output)
    except Exception:
        pass

    update_user_profile(user_id, {"last_query": user_query})
    
    return final_output
