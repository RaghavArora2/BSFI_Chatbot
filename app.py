import streamlit as st
import os
import tempfile
from insurance_chatbot import InsuranceChatbot
from knowledge_base import create_knowledge_base
from utils import display_chat_history, give_feedback

# Set the Google API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAQW3JngAxn3DqbZQWzvIT3kb2w098qI9c"

# Page configuration with improved layout
st.set_page_config(page_title="Insurance Advisor Chatbot",
                   page_icon="🛡️",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "documents" not in st.session_state:
    st.session_state.documents = {}  # Dictionary to store uploaded documents
if "active_document" not in st.session_state:
    st.session_state.active_document = None
if "chatbot" not in st.session_state:
    st.session_state.chatbot = None
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = set()  # To track which messages have received feedback

# Check for Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error(
        "Google API key not found. Please set the GOOGLE_API_KEY environment variable."
    )
    st.info(
        "Using Google's Gemini model requires an API key. You can get one for free at https://aistudio.google.com/app/apikey"
    )
else:
    try:
        # Initialize knowledge base with default documents if no custom documents are uploaded
        if not st.session_state.documents and st.session_state.chatbot is None:
            kb = create_knowledge_base()
            st.session_state.chatbot = InsuranceChatbot(kb)
            st.session_state.documents[
                "Default Insurance Policies"] = "Default"
            st.session_state.active_document = "Default Insurance Policies"
    except Exception as e:
        st.error(f"Error initializing chatbot: {str(e)}")


# Function to handle document upload and custom text input
def handle_document_upload():
    # Add tabs for different input methods
    tab1, tab2 = st.tabs(["Upload PDF", "Enter Custom Text"])

    with tab1:
        uploaded_file = st.file_uploader(
            "Upload insurance policy document (PDF)", type="pdf")

        if uploaded_file is not None:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False,
                                             suffix='.pdf') as tmp_file:
                # Write the uploaded file content to the temporary file
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            try:
                # Create knowledge base from the uploaded document
                kb = create_knowledge_base(custom_pdf_path=tmp_path)
                document_name = uploaded_file.name

                # Add to documents dictionary
                st.session_state.documents[document_name] = tmp_path
                st.session_state.active_document = document_name

                # Initialize chatbot with new knowledge base
                st.session_state.chatbot = InsuranceChatbot(kb)

                st.success(
                    f"Successfully uploaded and processed {document_name}")
                # Clean the chat history when changing documents
                st.session_state.chat_history = []

            except Exception as e:
                st.error(f"Error processing the uploaded document: {str(e)}")
            finally:
                # Clean up the temporary file
                import os
                os.unlink(tmp_path)

    with tab2:
        st.write("Enter your insurance information text below:")
        custom_text = st.text_area(
            "Insurance Information",
            height=300,
            placeholder="Paste your insurance policy text here...")

        if st.button("Process Custom Text"):
            if custom_text.strip():
                try:
                    # Create knowledge base from the custom text
                    kb = create_knowledge_base(custom_text=custom_text)
                    document_name = "Custom Text Input"

                    # Add to documents dictionary
                    st.session_state.documents[document_name] = "custom_text"
                    st.session_state.active_document = document_name

                    # Initialize chatbot with new knowledge base
                    st.session_state.chatbot = InsuranceChatbot(kb)

                    st.success("Successfully processed custom text")
                    # Clean the chat history when changing documents
                    st.session_state.chat_history = []

                except Exception as e:
                    st.error(f"Error processing custom text: {str(e)}")
            else:
                st.warning("Please enter some text before processing.")


# Apply custom styles for a more modern UI
st.markdown("""
<style>
/* Global Improvements */
.stApp {
    max-width: 1200px;
    margin: 0 auto;
}

/* Button styling */
.stButton button {
    background-color: #4169E1;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 500;
    border: none;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.stButton button:hover {
    background-color: #3151b5;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Input field styling */
.stTextInput input, .stTextArea textarea {
    border-radius: 8px;
    border: 1px solid #ddd;
    padding: 0.75rem;
    transition: all 0.3s ease;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #4169E1;
    box-shadow: 0 0 0 2px rgba(65,105,225,0.2);
}

/* Chat container styling */
.chat-container {
    border-radius: 12px;
    margin-bottom: 1.5rem;
    padding: 0.5rem;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 0.5rem 1rem;
}
.stTabs [aria-selected="true"] {
    background-color: #4169E1;
    color: white;
}

/* Sidebar improvements */
.stSidebar {
    padding-top: 2rem;
}
</style>
""",
            unsafe_allow_html=True)

# App header with improved styling
st.markdown(
    "<h1 style='text-align: center; margin-bottom: 1.5rem; color: #4169E1;'>🛡️ Insurance Advisor Chatbot</h1>",
    unsafe_allow_html=True)

# Sidebar for document management
with st.sidebar:
    st.header("Document Management")

    # Document uploader
    st.subheader("Upload Document")
    handle_document_upload()

    # Document switcher
    if st.session_state.documents:
        st.subheader("Switch Document")
        selected_document = st.selectbox(
            "Select Document",
            options=list(st.session_state.documents.keys()),
            index=list(st.session_state.documents.keys()).index(
                st.session_state.active_document)
            if st.session_state.active_document else 0)

        if selected_document != st.session_state.active_document:
            if st.session_state.documents[selected_document] == "Default":
                # Use default knowledge base
                kb = create_knowledge_base()
            elif st.session_state.documents[
                    selected_document] == "custom_text":
                # For previously saved custom text, we need to recreate from initial data
                # Here we're using the health insurance text from the attached assets
                with open(
                        "attached_assets/Pasted--Health-Insurance-Policies-Basic-Health-Insurance-Our-Basic-Health-Insurance-plan-offers-cover-1745422656700.txt",
                        "r") as f:
                    insurance_text = f.read()
                kb = create_knowledge_base(custom_text=insurance_text)
            else:
                # Create knowledge base from the custom document
                kb = create_knowledge_base(custom_pdf_path=st.session_state.
                                           documents[selected_document])

            # Initialize chatbot with the selected knowledge base
            st.session_state.chatbot = InsuranceChatbot(kb)
            st.session_state.active_document = selected_document
            st.session_state.chat_history = [
            ]  # Reset chat history when switching documents
            st.rerun()

# Main content area
st.markdown("""
    Welcome to the AI Insurance Assistant! Ask me questions about:
    - Health insurance policies
    - Life insurance coverage
    - Auto insurance details
    - Home insurance options
    - Premium calculations
    - Claims processes
""")

# Show active document
if st.session_state.active_document:
    st.info(f"Currently using: {st.session_state.active_document}")

# Display chat history with feedback buttons
display_chat_history(st.session_state.chat_history)


# Function to handle user message submission
def submit():
    if "temp_input" in st.session_state and st.session_state.temp_input:
        user_message = st.session_state.temp_input

        if st.session_state.chatbot is None:
            st.error(
                "Chatbot is not initialized. Please check the error above.")
            return

        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })

        with st.spinner("Thinking..."):
            try:
                # Get response from chatbot
                response = st.session_state.chatbot.get_response(user_message)

                # Add assistant message to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
            except Exception as e:
                st.session_state.chat_history.append({
                    "role":
                    "assistant",
                    "content":
                    f"I'm having trouble answering that. Error: {str(e)}"
                })

        # Clear the input for next message
        st.session_state.temp_input = ""


# Function to process FAQ questions
def process_faq(question):
    if st.session_state.chatbot is None:
        st.error("Chatbot is not initialized. Please check the error above.")
        return

    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": question})

    with st.spinner("Thinking..."):
        try:
            # Get response from chatbot
            response = st.session_state.chatbot.get_response(question)

            # Add assistant message to chat history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
        except Exception as e:
            st.session_state.chat_history.append({
                "role":
                "assistant",
                "content":
                f"I'm having trouble answering that. Error: {str(e)}"
            })

    st.rerun()


# Input area with FAQ section
with st.container():
    # Initialize temp_input if it doesn't exist
    if "temp_input" not in st.session_state:
        st.session_state.temp_input = ""

    # Text input that properly handles Enter key press
    st.text_input("Type your insurance question here:",
                  key="temp_input",
                  on_change=submit)

    col1, col2 = st.columns([5, 1])
    with col1:
        if st.button("Send", use_container_width=True):
            submit()

    with col2:
        if st.button("Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # FAQ section near input
    st.write("**Common Questions:**")
    faq_questions = [
        "What are the eligibility criteria for life insurance?",
        "How do I file a health insurance claim?",
        "What does auto liability insurance cover?",
        "What factors affect my home insurance premium?",
        "What is the difference between term and whole life insurance?",
        "How much coverage do I need for my car insurance?"
    ]

    # Display FAQ questions in columns of 2
    col1, col2 = st.columns(2)

    for i, question in enumerate(faq_questions):
        if i % 2 == 0:
            with col1:
                if st.button(question, key=f"faq_{i}"):
                    process_faq(question)
        else:
            with col2:
                if st.button(question, key=f"faq_{i}"):
                    process_faq(question)

# Footer
st.markdown("---")
st.markdown(
    "*This chatbot uses AI to provide information about insurance policies. For complex inquiries, please contact our customer service.*"
)