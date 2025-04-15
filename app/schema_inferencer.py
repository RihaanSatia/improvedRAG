from typing import List, Dict
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
from app.prompts import METADATA_PROMPT
import json
import streamlit as st
import re
import pdb
from dotenv import load_dotenv
load_dotenv()

def infer_table_metadata_from_columns(table_name: str, columns: List[Dict[str, str]]) -> Dict:
    column_list_str = "\n".join(f"- {col['name']}: {col['type']}" for col in columns)
    #print("this is the metadata prompt:" , METADATA_PROMPT)
    prompt = METADATA_PROMPT.format(table_name=table_name, column_list=column_list_str)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    messages = [
        ChatMessage(role="system", content="You are a helpful assistant."),
        ChatMessage(role="user", content=prompt)
    ]
    response = llm(messages)
    content = response.content
    #st.write(content)
    try:
        json_block = re.findall(r"```json(.*?)```", content, re.DOTALL)[0].strip()
        cleaned = re.sub(r",\s*([}\]])", r"\1", json_block)
        print("here is the content",content)
        return json.loads(cleaned)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to parse LLM response: {e}\n\n--- Raw content ---\n{content}")
