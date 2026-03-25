from rag.retriever import store_data

def store_strategy(user_id, query, strategy):
    structured = f"""
[STRATEGY]
User: {user_id}
Query: {query}
{strategy}
"""
    store_data(structured)


def store_market(user_id, trends, whitespace):
    structured = f"""
[MARKET]
User: {user_id}
Trends: {trends}
Whitespace: {whitespace}
"""
    store_data(structured)


def store_interaction(user_id, query):
    structured = f"""
[INTERACTION]
User: {user_id}
Query: {query}
"""
    store_data(structured)