import streamlit as st
from typing import List, Dict, Any

def display_chat_history(chat_history: List[Dict[str, Any]]):
    """
    Display the chat history in a visually appealing format with feedback buttons.

    Args:
        chat_history: List of message dictionaries with 'role' and 'content' keys
    """
    if not chat_history:
        st.info("Start a conversation by asking a question about insurance!")
        return

    # Create containers for chat messages
    chat_container = st.container()

    with chat_container:
        for idx, message in enumerate(chat_history):
            role = message["role"]
            content = message["content"]

            if role == "user":
                with st.chat_message("user", avatar="👤"):
                    st.write(content)

            elif role == "assistant":
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(content)

                    # Add feedback buttons for assistant messages
                    # Only add buttons for new messages that haven't received feedback
                    if "feedback_given" in st.session_state and idx not in st.session_state.feedback_given:
                        col1, col2, col3 = st.columns([1, 1, 10])
                        with col1:
                            if st.button("👍", key=f"thumbs_up_{idx}"):
                                give_feedback(idx, "positive")
                                st.rerun()
                        with col2:
                            if st.button("👎", key=f"thumbs_down_{idx}"):
                                give_feedback(idx, "negative")
                                st.rerun()
                        with col3:
                            st.write("Was this response helpful?")

# Function to handle feedback (defined in app.py, referenced here)
def give_feedback(msg_idx, feedback_type):
    """
    Process user feedback on chatbot responses.

    Args:
        msg_idx: Index of the message in chat history
        feedback_type: Type of feedback ("positive" or "negative")
    """
    if msg_idx not in st.session_state.feedback_given:
        # Add to the set of messages that have received feedback
        st.session_state.feedback_given.add(msg_idx)
        st.success(f"Thank you for your {feedback_type} feedback!")

        # Here you could implement additional logic to:
        # 1. Store feedback in a database
        # 2. Use feedback to improve the model
        # 3. Change responses based on negative feedback
