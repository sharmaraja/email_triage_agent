
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import LLM_MODEL, LLM_TEMPERATURE

llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)

prompt = ChatPromptTemplate.from_template("""
You are an email triage assistant. Analyze the following email and output ONLY a valid JSON object with:

- "sentiment": one of {sentiments} based on tone (positive: praise/enthusiasm; neutral: factual; negative: complaint/frustration)
- "urgency": one of {urgencies} (urgent: needs immediate action; non-urgent: routine; spam: promotional/irrelevant)
- "reasoning": 1-2 sentence explanation
- "draft_response": Suggested polite reply (50-150 words; empty string '' if spam or no-reply needed; personalize if possible)

Email: {email}

Output JSON only, no extra text.
""")

parser = JsonOutputParser()

analyze_chain = prompt | llm | parser