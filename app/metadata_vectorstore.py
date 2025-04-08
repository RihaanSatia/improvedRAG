import os
from typing import Dict, List, Optional
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import streamlit as st
import numpy as np

VECTORSTORE_PATH = os.path.join("data", "metadata_index")
DEFAULT_CONFIDENCE_THRESHOLD = 0.25

def store_descriptions_in_vectorstore(documents: list[Document]) -> None:
    os.makedirs(os.path.dirname(VECTORSTORE_PATH), exist_ok=True)
    vectorstore = FAISS.from_documents(documents, OpenAIEmbeddings())
    vectorstore.save_local(VECTORSTORE_PATH)

def get_confidence_summary(
            scored_matches: List[Dict],
            threshold: float
    ) -> Dict:
        if not scored_matches:
            return {
                'average_confidence': 0.0,
                'max_confidence': 0.0,
                'min_confidence': 0.0,
                'sufficient_confidence': False
            }
        
        scores = [match['confidence'] for match in scored_matches]
        return {
            'average_confidence': round(np.mean(scores), 3),
            'max_confidence': round(max(scores),3),
            'min_confidence': round(min(scores),3),
            'sufficient_confidence': max(scores) >= threshold
        }

def search_metadata_with_scores(query: str, k: int = 4, confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD) -> Dict:
    vectorstore = FAISS.load_local(
        VECTORSTORE_PATH,
        OpenAIEmbeddings(),
        allow_dangerous_deserialization=True
    )
    docs_and_scores = vectorstore.similarity_search_with_score(query, k=k)
    scored_matches = []
    st.write(docs_and_scores)
    for doc, score in docs_and_scores:
        confidence = float(score)
        
        if score >= confidence_threshold:
            scored_matches.append(
                {
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'confidence': round(confidence,3)
                }
            )
    scored_matches.sort(key = lambda x: x['confidence'], reverse=True)

    confidence_summary = get_confidence_summary(scored_matches, confidence_threshold)
    return {
        'matches': scored_matches,
        'confidence_summary': confidence_summary,
        'needs_clarification': not confidence_summary
        ['sufficient_confidence']
    }
    
    