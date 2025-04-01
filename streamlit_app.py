# streamlit_app.py

import streamlit as st
from app.rag_pipeline import run_rag_pipeline

st.set_page_config(page_title="Improved RAG Reasoning", layout="centered")

st.title("🧠 Improved RAG Reasoning Lab")
st.markdown("Ask a question about your data and see how the model reasons before answering.")

question = st.text_input("Enter your question:")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            response = run_rag_pipeline(question)
        st.markdown("### 💬 Answer")
        st.success(response)
