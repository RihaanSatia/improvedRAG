from app.rag_pipeline import run_rag_pipeline

if __name__ == "__main__":
    print("\nWelcome to Improved RAG Reasoning Lab 🧠")
    question = input("\nAsk a question about your data: ")
    response = run_rag_pipeline(question)
    print("\n---\nAnswer:")
    print(response)


### app/data_loader.py
import pandas as pd
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import CSVLoader
from langchain.schema.document import Document
import os

def load_csv_as_documents(filepath: str) -> list[Document]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    loader = CSVLoader(file_path=filepath)
    docs = loader.load()
    return docs

def split_documents(docs: list[Document], chunk_size=800, chunk_overlap=100) -> list[Document]:
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)