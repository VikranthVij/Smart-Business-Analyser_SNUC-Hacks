from rag.vector_store import VectorStore

vector_db = VectorStore()


# 🔹 STORE (no change)
def store_data(text):
    vector_db.add(text)


# 🔥 SPLIT MEMORY RETRIEVAL
def retrieve_context(query):
    results = vector_db.search(query)

    strategy = []
    market = []
    interaction = []

    for r in results:
        if "[STRATEGY]" in r:
            strategy.append(r)
        elif "[MARKET]" in r:
            market.append(r)
        elif "[INTERACTION]" in r:
            interaction.append(r)

    return {
        "strategy": strategy,
        "market": market,
        "interaction": interaction
    }