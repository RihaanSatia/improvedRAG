from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document

_vectorstore = None


def build_vectorstore(docs: list[Document]):
    global _vectorstore
    embedding = OpenAIEmbeddings()
    _vectorstore = FAISS.from_documents(docs, embedding)

def get_retriever():
    if _vectorstore is None:
        raise ValueError("Vectorstore not initialized.")
    return _vectorstore.as_retriever()
