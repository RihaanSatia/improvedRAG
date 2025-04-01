import json
import re
from typing import List
from langchain.chat_models import ChatOpenAI
from app.prompt_templates import TABLE_RERANKER_INSTRUCTION


def rerank_tables(user_query: str, table_descriptions: List[str]) -> List[str]:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    formatted_tables = "\n\n".join(table_descriptions)
    prompt = TABLE_RERANKER_INSTRUCTION.format(query=user_query, tables=formatted_tables)

    response = llm.predict(prompt)

    try:
        json_str = re.findall(r"\[.*\]", response, re.DOTALL)[0]
        return json.loads(json_str)
    except Exception as e:
        print("Error parsing LLM response:", e)
        print("Raw response:", response)
        return []