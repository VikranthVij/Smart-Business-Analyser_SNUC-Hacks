import os

os.environ["GROQ_API_KEY"] = ""




from prompts.strategy_prompt import get_prompt
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from config import MODEL_NAME, TEMPERATURE

llm = ChatGroq(
    model=MODEL_NAME,
    temperature=TEMPERATURE
)

def generate_strategy(context, rules_output, tone):
    prompt = get_prompt()

    chain = prompt | llm

    response = chain.invoke({
        "trends": context["trends"],
        "overused": context["overused"],
        "whitespace": context["whitespace"],
        "actions": context["actions"],
        "flags": rules_output["strategy_flags"],
        "segments": rules_output["priority_segments"],
        "tone": tone
    })

    return response.content