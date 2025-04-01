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

TABLE_RERANKER_INSTRUCTION = PromptTemplate.from_template("""
You are a database expert. Your job is to select the most relevant tables based on a user query.
Below are table descriptions. Return the most relevant ones as a JSON list.

User Query:
{query}

Table Descriptions:
{tables}

Return JSON list of table names.
""")