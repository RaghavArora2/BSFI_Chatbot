import streamlit as st
from typing import List, Dict, Any

def display_chat_history(chat_history: List[Dict[str, Any]]):
    """
    Display the chat history in a visually appealing format with feedback buttons.

    Args:
        chat_history: List of message dictionaries with 'role' and 'content' keys
    """
    if not chat_history:
        return
    
    chat_container = st.container()
    
    with chat_container:
        for idx, message in enumerate(chat_history):
            role = message["role"]
            content = message["content"]
            
            if role == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(f"""<div class="user-message">{content}</div>""", unsafe_allow_html=True)
            
            elif role == "assistant":
                is_new_message = (idx == len(chat_history) - 1 and 
                                role == "assistant" and 
                                "displayed_messages" in st.session_state and
                                idx not in st.session_state.displayed_messages)
                
                with st.chat_message("assistant", avatar="🤖"):
                    if is_new_message:
                        typing_placeholder = st.empty()
                        displayed_text = ""
                        for i in range(len(content) + 1):
                            displayed_text = content[:i]
                            typing_placeholder.markdown(
                                f"""<div class="assistant-message typing-effect">{displayed_text}</div>""", 
                                unsafe_allow_html=True
                            )
                            if i < len(content):
                                if len(content) > 500:
                                    import time
                                    time.sleep(0.001)
                                elif len(content) > 200:
                                    import time
                                    time.sleep(0.005)
                                else:
                                    import time
                                    time.sleep(0.01)
                        
                        if "displayed_messages" not in st.session_state:
                            st.session_state.displayed_messages = set()
                        st.session_state.displayed_messages.add(idx)
                    else:
                        st.markdown(f"""<div class="assistant-message">{content}</div>""", unsafe_allow_html=True)
                    
                    if "feedback_given" in st.session_state and idx not in st.session_state.feedback_given:
                        feedback_container = st.container()
                        with feedback_container:
                            col1, col2, col3 = st.columns([1, 1, 10])
                            with col1:
                                if st.button("👍", key=f"thumbs_up_{idx}"):
                                    give_feedback(idx, "positive")
                            with col2:
                                if st.button("👎", key=f"thumbs_down_{idx}"):
                                    give_feedback(idx, "negative")
                            with col3:
                                st.markdown("<span style='color:#777; font-size:0.8rem;'>Was this response helpful?</span>", unsafe_allow_html=True)

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
        st.session_state.feedback_given.add(msg_idx)
        
        if feedback_type == "positive":
            st.success("Thank you for your feedback! We're glad this response was helpful.")
        else:
            st.info("Thank you for your feedback. We'll work to improve our responses.")

        import time
        time.sleep(0.5)
        st.rerun() 