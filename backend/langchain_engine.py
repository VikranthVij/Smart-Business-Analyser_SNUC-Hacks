from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

# ==============================
# LLM SETUP
# ==============================
llm = ChatOpenAI(
    temperature=0.3,
    model="gpt-3.5-turbo"
)

# ==============================
# PROMPT TEMPLATE (UPGRADED)
# ==============================
template = """
You are an expert business intelligence analyst.

Market Trend:
{trend}

Customer Issues:
{issues}

Ad Signals:
{ads}

Analyze and provide:

1. Key Insight
2. Opportunity (where to enter market)
3. Strategy (how to win)
4. Risk (what could go wrong)

Be sharp, realistic, and actionable.
"""

prompt = PromptTemplate(
    input_variables=["trend", "issues", "ads"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)


# ==============================
# MAIN FUNCTION
# ==============================
def generate_ai_insight(trend, issues, ads):
    try:
        return chain.run({
            "trend": trend,
            "issues": issues,
            "ads": ads
        })
    except Exception as e:
        return f"⚠️ AI insight unavailable: {str(e)}"