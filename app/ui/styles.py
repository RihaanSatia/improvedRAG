CHAT_UI_STYLES = """
    /* Font Awesome Import */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    
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
        height: calc(100vh - 200px);  /* Adjusted height */
        overflow-y: auto;
        padding-bottom: 1rem;
        margin-bottom: 60px;  /* Reduced margin */
    }

    /* Message styling */
    .user-message {
        background-color: rgba(46, 103, 167, 0.8);  /* Translucent blue */
        color: #E8F0F8;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
        backdrop-filter: blur(10px);
    }

    .assistant-message {
        background-color: #dfe3e8;  /* Translucent light blue-gray */
        color: #2C3E50;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        max-width: 80%;
        backdrop-filter: blur(10px);
    }

    /* Status styling */
    .status-success {
        background-color: #a1b3c7;  /* Light green background */
        color: #404f61;  
        padding: 0.3rem 0.5rem;
        border-radius: 8px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }

    /* Input container */
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: transparent;  /* Changed to transparent */
        padding: 1rem;  /* Reduced padding */
        z-index: 1000;
    }

    /* Input and button styling */
    .input-column .stTextInput input {
        border: 1px solid #e6e6e6;
        border-radius: 8px;
        padding: 12px 16px;
        height: 50px;
        margin: 0;  /* Removed vertical margin */
        font-size: 16px;
    }

    .button-column button {
        background-color: #2E67A7;
        color: white;
        height: 50px;
        margin: 0;  /* Removed vertical margin */
        border-radius: 8px;
        font-size: 16px;
        padding: 0 1.5rem;
    }

    /* Add hover effect to button */
    .button-column button:hover {
        background-color: #245686;
        transition: background-color 0.2s ease;
    }

    /* Hide Streamlit's bottom padding */
    .css-1dp5vir {
        padding-bottom: 0 !important;
    }
"""
