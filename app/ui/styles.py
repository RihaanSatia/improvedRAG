CHAT_UI_STYLES = """
    /* Main container adjustments */
    .main {
        padding: 1.5rem !important;
        padding-bottom: 0 !important;
    }

    /* Hide default streamlit margins */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin: 0 !important;
    }

    /* Title container */
    .title-container {
        margin-bottom: 1rem;
    }

    /* Chat messages container */
    .chat-container {
        height: calc(100vh - 280px);
        overflow-y: auto;
        padding-bottom: 1rem;
        margin-bottom: 80px;
    }

    /* Message styling */
    .user-message {
        background-color: #0078D4;
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
    }

    .assistant-message {
        background-color: #f0f2f6;
        color: black;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        max-width: 80%;
    }

    /* Fixed input container */
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 1rem 2rem;
        border-top: 1px solid #e6e6e6;
        z-index: 1000;
    }

    /* Input and button styling */
    .input-column .stTextInput input {
        border: 1px solid #e6e6e6;
        padding: 8px 12px;
        height: 45px;
    }

    .button-column button {
        background-color: #0078D4;
        color: white;
        height: 45px;
        margin-top: 0;
    }
"""
