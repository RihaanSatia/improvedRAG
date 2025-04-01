from langchain.prompts import PromptTemplate



BASELINE_PROMPT = PromptTemplate.from_template("""
Answer the question using only the context below:

{context}

Question: {question}
Answer:
""")

REASONING_PROMPT = PromptTemplate.from_template("""
You are a careful, reasoning-first assistant.
Before answering, think step-by-step.

Context:
{context}

Question: {question}
Think through the answer carefully, then respond:
""")