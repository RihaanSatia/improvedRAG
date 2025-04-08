from app.rag_pipeline import run_rag_pipeline


if __name__ == "__main__":
    print("\nWelcome to Improved RAG Reasoning Lab 🧠")
    question = input("\nAsk a question about your data: ")
    response = run_rag_pipeline(question)
    print("\n---\nAnswer:")
    print(response)