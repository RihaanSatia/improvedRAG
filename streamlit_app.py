import streamlit as st
from app.rag_pipeline import run_rag_pipeline
import warnings
warnings.filterwarnings("ignore")

# Page config with custom theme
st.set_page_config(
    page_title="RAG Reasoning Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for chat-like interface
st.markdown("""
    <style>
    /* Reset default Streamlit styles */
    .main > div {
        padding-bottom: 0 !important;
    }
    
    .stApp {
        margin: 0;
        padding: 0;
    }

    /* Main container styles */
    .main {
        padding: 0;
        margin: 0;
        height: 100vh;
        overflow: hidden;
    }

    /* Title container */
    .title-container {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        padding: 1rem 2rem;
        background: white;
        z-index: 100;
    }

    /* Chat container with scrolling */
    .chat-container {
        position: fixed;
        top: 80px;  /* Adjust based on your title height */
        bottom: 80px;  /* Height of input container */
        left: 0;
        right: 0;
        overflow-y: auto;
        padding: 1rem 2rem;
    }

    /* Fixed chat input container */
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 80px;
        background-color: white;
        padding: 1rem 2rem;
        border-top: 1px solid #dee2e6;
        z-index: 1000;
    }

    /* Message styles */
    .user-message {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
    }

    .assistant-message {
        background-color: #007bff;
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        max-width: 80%;
        margin-right: auto;
    }

    /* Custom scrollbar */
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }

    .chat-container::-webkit-scrollbar-track {
        background: #f1f1f1;
    }

    .chat-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 3px;
    }

    .chat-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }

    /* Hide Streamlit default elements */
    .stDeployButton, footer {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for configurations
with st.sidebar:
    st.title("⚙️ Configuration")
    error_rate = st.slider(
        "Error Rate",
        min_value=0.0,
        max_value=1.0,
        value=0.9,
        help="Higher values mean stricter matching criteria"
    )
    
    show_metadata = st.checkbox(
        "Show Metadata",
        value=False,
        help="Display additional information about the matching process"
    )
    
    st.markdown("---")
    st.markdown("""
        ### About
        This RAG (Retrieval Augmented Generation) system uses:
        - Conformal prediction for reliable retrieval
        - Calibrated confidence scoring
        - Advanced metadata matching
    """)
    
    # Moved repository link to sidebar
    st.markdown("---")
    st.markdown(
        "[Repository](https://github.com/RihaanSatia/improvedRAG)",
        unsafe_allow_html=True
    )

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat title in fixed container
st.markdown('<div class="title-container">', unsafe_allow_html=True)
st.title("🤖 RAG Reasoning Assistant")
st.markdown('</div>', unsafe_allow_html=True)

# Display chat history in scrollable container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{message["content"]}', unsafe_allow_html=True)
        if show_metadata and "metadata" in message:
            st.markdown('<div class="metadata-box">', unsafe_allow_html=True)
            st.markdown("**Matched Columns:**")
            for match in message["metadata"].get("matches", []):
                st.markdown(f"- {match}")
            if "scores" in message["metadata"]:
                st.markdown("**Confidence Scores:**")
                for score in message["metadata"]["scores"]:
                    st.markdown(f"- {score:.3f}")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Fixed chat input at bottom
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
col1, col2 = st.columns([6, 1])
with col1:
    question = st.text_input(
        "Chat input",
        placeholder="Ask a question about your data...",
        key="chat_input"
    )
with col2:
    send_button = st.button("➤", key="send", help="Send message")
st.markdown('</div>', unsafe_allow_html=True)

if send_button and question.strip():
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Create a placeholder for technical output
    tech_output = st.empty()
    
    # Get RAG response with verbose output
    with st.spinner(""):
        # Show technical details in an expander
        with st.expander("Technical Details", expanded=False):
            response = run_rag_pipeline(
                question,
                error_rate=error_rate,
                verbose=True  # Enable verbose output
            )
    
    # Add assistant response to chat
    message_content = response.get('message', str(response))
    metadata = {
        "matches": response.get('matches', []),
        "scores": response.get('scores', [])
    } if isinstance(response, dict) else {}
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": message_content,
        "metadata": metadata
    })
    
    # Rerun to update chat display
    st.rerun()

# Footer section removed as we moved it to sidebar
