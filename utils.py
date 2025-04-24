import streamlit as st
from typing import List, Dict, Any

def display_chat_history(chat_history: List[Dict[str, Any]]):
    """
    Display the chat history in a visually appealing format.

    Args:
        chat_history: List of message dictionaries with 'role' and 'content' keys
    """
    if not chat_history:
        return
    
    # Create containers for chat messages
    chat_container = st.container()
    
    # Initialize displayed_messages if not exists
    if "displayed_messages" not in st.session_state:
        st.session_state.displayed_messages = set()
    
    # Add anchor for scroll position
    if "maintain_position" in st.session_state and st.session_state.maintain_position:
        st.markdown('<div id="maintain_position"></div>', unsafe_allow_html=True)
        # Reset flag
        st.session_state.maintain_position = False
    
    with chat_container:
        for idx, message in enumerate(chat_history):
            role = message["role"]
            content = message["content"]
            
            # Fix for "explain in detail" responses
            if content.lower().strip() == "explain in detail":
                content = "Please explain this in more detail."
            
            if role == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(f"""<div class="user-message">{content}</div>""", unsafe_allow_html=True)
            
            elif role == "assistant":
                # Check if this is the newest message and hasn't been displayed with typing effect
                is_new_message = (idx == len(chat_history) - 1 and 
                                 role == "assistant" and 
                                 idx not in st.session_state.displayed_messages)
                
                with st.chat_message("assistant", avatar="🤖"):
                    # Apply typing effect for new assistant messages
                    if is_new_message:
                        typing_placeholder = st.empty()
                        displayed_text = ""
                        typing_speed = 0.01  # Base typing speed
                        
                        # Adjust typing speed based on content length
                        if len(content) > 500:
                            typing_speed = 0.0005  # Very fast for long messages
                        elif len(content) > 200:
                            typing_speed = 0.002   # Fast for medium messages
                        
                        # Process content in chunks for improved performance
                        chunk_size = 5  # Characters per chunk
                        for i in range(0, len(content) + chunk_size, chunk_size):
                            end_pos = min(i, len(content))
                            displayed_text = content[:end_pos]
                            typing_placeholder.markdown(
                                f"""<div class="assistant-message typing-effect">{displayed_text}</div>""", 
                                unsafe_allow_html=True
                            )
                            if end_pos < len(content):
                                import time
                                time.sleep(typing_speed)
                        
                        # Mark as displayed
                        st.session_state.displayed_messages.add(idx)
                    else:
                        # Regular display for already shown messages
                        st.markdown(f"""<div class="assistant-message">{content}</div>""", unsafe_allow_html=True)
    
    return False  # No rerun needed

def give_feedback(msg_idx, feedback_type):
    """
    Process user feedback on chatbot responses.

    Args:
        msg_idx: Index of the message in chat history
        feedback_type: Type of feedback ("positive" or "negative")
    """
    if "feedback_given" not in st.session_state:
        st.session_state.feedback_given = set()
        
    if msg_idx not in st.session_state.feedback_given:
        # Add to the set of messages that have received feedback
        st.session_state.feedback_given.add(msg_idx)
        
        # Store feedback message to display after rerun
        if feedback_type == "positive":
            st.session_state.feedback_message = {"type": "success", "text": "Thank you for your feedback! We're glad this response was helpful."}
        else:
            st.session_state.feedback_message = {"type": "info", "text": "Thank you for your feedback. We'll work to improve our responses."}
        
        # Here you could implement additional logic to:
        # 1. Store feedback in a database
        # 2. Use feedback to improve the model
        # 3. Change responses based on negative feedback
        
        # Set flag to maintain scroll position
        st.session_state.maintain_position = True
        
        # Don't call st.rerun() here - it will be handled in app.py