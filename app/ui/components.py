import streamlit as st
from .styles import CHAT_UI_STYLES

def init_page():
    """Initialize page configuration"""
    st.set_page_config(
        page_title="RAG Reasoning Assistant",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(f"<style>{CHAT_UI_STYLES}</style>", unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar with configurations"""
    with st.sidebar:
        st.title("⚙️ Configuration")
        error_rate = st.slider(
            "Error Rate",
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            help="Higher values mean stricter matching criteria"
        )
        
        st.markdown("---")
        st.markdown("""
            ### About
            This RAG system enhances answer reliability through conformal prediction and confidence scoring.
            
            Error Rate (0-1):
            - Lower (0.1): More permissive matching
            - Higher (0.9): Stricter matching, fewer but more confident results
        """)
        
        st.markdown("---")
        st.markdown(
            "<a href='https://github.com/RihaanSatia/improvedRAG' target='_blank'><i class='fab fa-github' style='font-size: 24px; color: #333;'></i></a>",
            unsafe_allow_html=True)
        
        return error_rate

def render_chat_messages(messages, show_metadata=False):
    """Render chat messages"""
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in messages:
            if message["role"] == "user":
                st.markdown(
                    f'<div class="user-message">{message["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="assistant-message">{message["content"]}</div>',
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)

def render_chat_input():
    """Render chat input and send button"""
    # Create fixed bottom container
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    
    # Create columns with specific classes
    col1, col2 = st.columns([6, 1])
    
    # Initialize the chat input key in session state if it doesn't exist
    if "chat_input_key" not in st.session_state:
        st.session_state.chat_input_key = 0
    
    with col1:
        st.markdown('<div class="input-column">', unsafe_allow_html=True)
        question = st.text_input(
            "Message",
            key=f"chat_input_{st.session_state.chat_input_key}",
            label_visibility="collapsed",
            placeholder="Ask a question about your data..."
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="button-column">', unsafe_allow_html=True)
        send_button = st.button("Send", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle input clearing by incrementing the key
    if send_button and question:
        st.session_state.chat_input_key += 1
    
    return question, send_button
