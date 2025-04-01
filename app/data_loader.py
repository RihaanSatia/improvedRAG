import pandas as pd
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import CSVLoader
from langchain.schema.document import Document
import os

def load_csv_as_documents(filepath: str) -> list[Document]:
    try:
        df = pd.read_csv(filepath, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="ISO-8859-1")

    docs = []
    for i, row in df.iterrows():
        content = "\n".join(f"{col}: {val}" for col, val in row.items())
        docs.append(Document(page_content=content))

    return docs

def split_documents(docs: list[Document], chunk_size=800, chunk_overlap=100) -> list[Document]:
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)