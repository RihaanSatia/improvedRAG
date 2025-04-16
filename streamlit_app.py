import streamlit as st
from app.rag_pipeline import run_rag_pipeline
from app.ui.components import init_page, render_sidebar, render_chat_messages, render_chat_input
import warnings
warnings.filterwarnings("ignore")

# Initialize page with configuration and styles
init_page()

# Get configurations from sidebar
error_rate = render_sidebar()

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat title in fixed container
st.markdown('<div class="title-container">', unsafe_allow_html=True)
st.title("RAG Reasoning Assistant")
st.markdown('</div>', unsafe_allow_html=True)

# Display chat messages
render_chat_messages(st.session_state.messages)

# Get user input
question, send_button = render_chat_input()

if send_button and question.strip():
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Get RAG response with verbose output
    with st.spinner(""):
        response = run_rag_pipeline(
            question,
            error_rate=error_rate,
            verbose=True
        )
        
        # Format the assistant's response
        def format_response(response):
            if not isinstance(response, dict):
                return str(response)
            
            formatted_message = []
            
            # Add status with new styling
            if response.get('status'):
                formatted_message.append(f'<div class="status-success">{response["status"]}</div>')
            
            # Add matches
            if response.get('matches'):
                formatted_message.append("\n### Relevant Matches")
                for match in response['matches']:
                    formatted_message.append(f"""
- Column: <span style='color: #808080'>{match['metadata']['column_name']}</span>
  - Content: {match['content']}
  - Table: <span style='color: #808080'>{match['metadata']['table_name']}</span>
  - Confidence: {(1 - match['cosine_distance']):.3f}
""")
            
            # Add confidence summary
            if response.get('confidence_summary'):
                summary = response['confidence_summary']
                formatted_message.append("\n### Confidence Metrics")
                formatted_message.append(f"""
- Average Confidence: {summary['average_confidence']:.3f}
- Maximum Confidence: {summary['max_confidence']:.3f}
- Minimum Confidence: {summary['min_confidence']:.3f}
- Number of Matches: {summary['num_chunks']}
""")
            
            # Add configuration details
            formatted_message.append("\n### Configuration")
            formatted_message.append(f"""
- Error Rate: {response.get('error_rate', 'N/A')}
- Confidence Level: {response.get('confidence_level', 'N/A'):.1f}%
""")
            
            return "\n".join(formatted_message)
        
        # Add assistant response to chat
        message_content = format_response(response)
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
