import os
import streamlit as st
import time
import datetime
from utils.document_processor import load_documents, create_vector_store
from utils.chat_utils import get_gemini_response
from utils.session_manager import (
    initialize_session_state, 
    load_knowledge_base, 
    add_message, 
    clear_chat_history,
    is_knowledge_base_loaded,
    record_query
)
from utils.evaluation import assess_response_quality, analyze_query_difficulty

# Set page configuration
st.set_page_config(
    page_title="Insurance Policy Assistant",
    page_icon="💬",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Update current time for logging
st.session_state._current_time = datetime.datetime.now().isoformat()

# App header and description
st.title("Insurance Policy Assistant")
st.markdown("""
This AI-powered assistant can help answer your questions about insurance policies.
Ask about coverage options, premiums, claim processes, and more for health, life, auto, and home insurance.
""")

# Initialize knowledge base if not already loaded
if not is_knowledge_base_loaded():
    if load_knowledge_base():
        st.success("Knowledge base initialized successfully!")
    else:
        st.warning("Failed to initialize knowledge base. Some features may not work properly.")

# Sidebar with configuration options
with st.sidebar:
    st.header("About")
    st.markdown("""
    This Insurance Policy Assistant uses AI to provide accurate information about different insurance policies.
    It references a knowledge base of insurance policy documents to answer your questions.
    
    **Sample Topics:**
    - Health insurance coverage and benefits
    - Auto insurance premiums and coverage options
    - Home insurance claims process
    - Life insurance policy types and selection
    - Insurance terminology explanations
    """)
    
    # Add section divider
    st.markdown("---")
    
    # Advanced options section
    st.header("Options")
    
    # Add option to reload knowledge base
    if st.button("🔄 Reload Knowledge Base"):
        st.session_state.document_loaded = False
        if load_knowledge_base():
            st.success("Knowledge base reloaded successfully!")
        else:
            st.warning("Failed to reload knowledge base.")
    
    # Display information about the model
    st.markdown("---")
    st.header("Model Information")
    st.markdown("Using **Google Gemini** for natural language processing.")
    st.markdown("""
    - **Knowledge Base:** Insurance policy documents
    - **Last Updated:** Auto-updated on startup
    """)
    
    # Add option to clear chat history
    if st.button("🗑️ Clear Chat History"):
        clear_chat_history()
        st.success("Chat history cleared!")
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about insurance policies..."):
    # Add user message to chat history
    add_message("user", prompt)
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        if not is_knowledge_base_loaded():
            st.warning("Knowledge base not loaded. Please reload the knowledge base.")
            response = "I'm unable to access the insurance policy information at the moment. Please try reloading the knowledge base."
            add_message("assistant", response)
        else:
            message_placeholder = st.empty()
            full_response = ""
            
            # Analyze query difficulty (for logging/metrics)
            difficulty = analyze_query_difficulty(prompt)
            
            # Display typing indicator
            with st.spinner("Searching insurance knowledge base..."):
                # Get response from Gemini with context from the vector store
                response_generator = get_gemini_response(
                    prompt, 
                    st.session_state.vector_store,
                    st.session_state.messages
                )
                
                # Display the response word by word for a more natural feel
                for chunk in response_generator:
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.01)
                
                # Display final response
                message_placeholder.markdown(full_response)
                
                # Assess response quality (for logging/metrics)
                quality_metrics = assess_response_quality(prompt, full_response)
                
                # Record the query, response, and metrics
                record_query(
                    query=prompt,
                    response=full_response,
                    feedback={
                        "difficulty": difficulty,
                        "quality_metrics": quality_metrics
                    }
                )
                
                # Add response to chat history
                add_message("assistant", full_response)
    
    # Add a small gap after each message
    st.markdown("")

# Additional helpful guidelines (only shown when chat is empty)
if not st.session_state.messages:
    st.markdown("---")
    st.markdown("### How to use this assistant")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Example questions you can ask:**
        - What does auto insurance typically cover?
        - How are health insurance premiums calculated?
        - What's the process for filing a home insurance claim?
        - What's the difference between term and whole life insurance?
        - What factors affect my insurance rates?
        """)
    
    with col2:
        st.markdown("""
        **Topics covered:**
        - Auto/car insurance
        - Health/medical insurance
        - Home/property insurance
        - Life insurance policies
        - Insurance terms and concepts
        - Claims processes
        """)

# Footer
st.markdown("---")
st.markdown(
    "This chatbot is for informational purposes only. For specific policy details, please contact your insurance provider."
)
