from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from app.prompt_templates import REASONING_PROMPT
from app.data_loader import load_csv_as_documents, split_documents
from app.vectorstore import build_vectorstore, get_retriever
import os
from dotenv import load_dotenv
load_dotenv()


# Change this path to your actual CSV

DATA_PATH = os.path.join("data", "Top10_CreditUnions1.csv")


def run_rag_pipeline(user_question: str) -> str:
    docs = load_csv_as_documents(DATA_PATH)
    chunks = split_documents(docs)
    build_vectorstore(chunks)

    retriever = get_retriever()
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": REASONING_PROMPT},
        return_source_documents=False
    )

    result = qa.run(user_question)
    return result