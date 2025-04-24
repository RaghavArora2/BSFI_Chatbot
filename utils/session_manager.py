"""
Session management utilities for the insurance policy chatbot.
This module handles Streamlit session state management and initialization.
"""

import streamlit as st
from typing import Dict, List, Optional, Any
from utils.document_processor import load_documents, create_vector_store

def initialize_session_state():
    """
    Initialize all required session state variables if they don't exist.
    This ensures all necessary state is available throughout the application.
    """
    # Chat message history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Vector store for document search
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    
    # Document loading status
    if "document_loaded" not in st.session_state:
        st.session_state.document_loaded = False
    
    # Chat context for maintaining conversation history
    if "conversation_context" not in st.session_state:
        st.session_state.conversation_context = []
    
    # Query history for tracking user questions
    if "query_history" not in st.session_state:
        st.session_state.query_history = []
    
    # Feedback collection
    if "feedback_collected" not in st.session_state:
        st.session_state.feedback_collected = {}

def add_message(role: str, content: str) -> None:
    """
    Add a message to the chat history.
    
    Args:
        role (str): The role of the message sender ('user' or 'assistant')
        content (str): The content of the message
    """
    message = {"role": role, "content": content}
    st.session_state.messages.append(message)
    
    # Also add to conversation context with limited history
    st.session_state.conversation_context.append(message)
    # Keep last 10 messages for context
    if len(st.session_state.conversation_context) > 10:
        st.session_state.conversation_context = st.session_state.conversation_context[-10:]

def get_last_n_messages(n: int = 5) -> List[Dict[str, str]]:
    """
    Get the last n messages from the chat history.
    
    Args:
        n (int): Number of messages to retrieve
        
    Returns:
        List[Dict[str, str]]: Last n messages
    """
    return st.session_state.messages[-n:] if len(st.session_state.messages) >= n else st.session_state.messages

def clear_chat_history() -> None:
    """Clear all messages from the chat history"""
    st.session_state.messages = []
    st.session_state.conversation_context = []
    st.session_state.query_history = []

def load_knowledge_base(directory_path: str = "sample_insurance_policies") -> bool:
    """
    Load the knowledge base from documents and create the vector store.
    
    Args:
        directory_path (str): Path to the directory containing documents
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with st.spinner("Loading insurance policy documents and creating knowledge base..."):
            # Load documents
            documents = load_documents(directory_path)
            if not documents:
                st.error("No documents found in the specified directory.")
                return False
            
            # Create vector store
            vector_store = create_vector_store(documents)
            if vector_store is None:
                st.error("Failed to create vector store from documents.")
                return False
            
            # Update session state
            st.session_state.vector_store = vector_store
            st.session_state.document_loaded = True
            
            return True
    except Exception as e:
        st.error(f"Error loading knowledge base: {str(e)}")
        return False

def record_query(query: str, response: str, feedback: Optional[str] = None) -> None:
    """
    Record a user query and the system's response for analysis.
    
    Args:
        query (str): The user's query
        response (str): The system's response
        feedback (Optional[str]): User feedback about the response, if provided
    """
    st.session_state.query_history.append({
        "query": query,
        "response": response,
        "timestamp": st.session_state.get("_current_time", None),
        "feedback": feedback
    })

def get_vector_store():
    """
    Get the current vector store from session state.
    
    Returns:
        The vector store object or None if not initialized
    """
    return st.session_state.vector_store if st.session_state.document_loaded else None

def is_knowledge_base_loaded() -> bool:
    """
    Check if the knowledge base is loaded and ready to use.
    
    Returns:
        bool: True if loaded, False otherwise
    """
    return st.session_state.document_loaded and st.session_state.vector_store is not None
