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
                   initial_sidebar_state="collapsed")  # Start with collapsed sidebar

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
if "show_document_upload" not in st.session_state:
    st.session_state.show_document_upload = False  # Flag to control document upload visibility

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


# Function to handle document upload
def handle_document_upload():
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


# Apply custom styles for a modern UI with animated borders
st.markdown("""
<style>
/* Global Improvements */
.stApp {
    max-width: 1200px;
    margin: 0 auto;
    background-color: #f8f9fa;
}

/* Container for the entire chat area */
.chat-container {
    background-color: white;
    border-radius: 20px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.08);
    padding: 20px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
    transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.chat-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(65,105,225,0.15);
}

/* Add animated border effect */
.chat-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 20px;
    padding: 3px;
    background: linear-gradient(
        135deg,
        rgba(65,105,225,0.6),
        rgba(0,191,255,0.6),
        rgba(138,43,226,0.4),
        rgba(65,105,225,0.6)
    );
    background-size: 300% 300%;
    -webkit-mask: 
        linear-gradient(#fff 0 0) content-box, 
        linear-gradient(#fff 0 0);
    -webkit-mask-composite: destination-out;
    mask-composite: exclude;
    animation: border-pulse 8s ease-in-out infinite;
    z-index: 0;
}

@keyframes border-pulse {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

/* Prevent UI glitches */
div[data-testid="stDecoration"], div[data-testid="stToolbar"] {
    z-index: 999;
}

/* Button styling with better animations */
.stButton button {
    background-color: #4169E1;
    color: white;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    font-weight: 500;
    border: none;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 12px rgba(65,105,225,0.2);
    position: relative;
    overflow: hidden;
}

.stButton button::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255,255,255,0.2),
        transparent
    );
    transition: all 0.4s ease;
}

.stButton button:hover {
    background-color: #3151b5;
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 15px rgba(65,105,225,0.3);
}

.stButton button:hover::after {
    left: 100%;
}

.stButton button:active {
    transform: translateY(1px) scale(0.98);
    box-shadow: 0 2px 8px rgba(65,105,225,0.3);
}

/* Input field styling with enhanced animation */
.stTextInput input {
    border-radius: 12px;
    border: 1px solid #e0e5eb;
    padding: 1.1rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    background-color: #f9fafc;
}

.stTextInput input:focus {
    border-color: #4169E1;
    box-shadow: 0 0 0 3px rgba(65,105,225,0.2);
    background-color: #fff;
    transform: translateY(-2px);
}

/* Message styling with better animations */
.user-message {
    background-color: #E9F0FF;
    border-radius: 15px;
    padding: 14px 18px;
    margin-bottom: 15px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    position: relative;
    animation: userMessageIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border-bottom-right-radius: 4px;
}

.assistant-message {
    background-color: #FFFFFF;
    border-radius: 15px;
    padding: 14px 18px;
    margin-bottom: 15px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    border-left: 4px solid #4169E1;
    position: relative;
    animation: assistantMessageIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border-bottom-left-radius: 4px;
}

@keyframes userMessageIn {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.9);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes assistantMessageIn {
    from {
        opacity: 0;
        transform: translateY(20px) scale(0.9);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* Add message hover effect */
.user-message:hover, .assistant-message:hover {
    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    transform: translateY(-2px);
    transition: all 0.3s ease;
}

/* Sidebar improvements */
.stSidebar {
    background-color: #ffffff;
    padding-top: 2rem;
    box-shadow: inset -1px 0 5px rgba(0,0,0,0.05);
}

/* Header styling with animation */
.main-header {
    text-align: center;
    color: #4169E1;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    position: relative;
    display: inline-block;
    animation: headerPulse 2s ease-in-out infinite alternate;
}

@keyframes headerPulse {
    from {
        text-shadow: 0 0 5px rgba(65, 105, 225, 0);
    }
    to {
        text-shadow: 0 0 12px rgba(65, 105, 225, 0.4);
    }
}

.main-header::after {
    content: '';
    position: absolute;
    width: 60%;
    height: 3px;
    background: linear-gradient(90deg, transparent, #4169E1, transparent);
    left: 20%;
    bottom: -10px;
    border-radius: 2px;
    animation: headerBorderPulse 3s ease-in-out infinite;
}

@keyframes headerBorderPulse {
    0% {
        opacity: 0.6;
        width: 40%;
        left: 30%;
    }
    50% {
        opacity: 1;
        width: 70%;
        left: 15%;
    }
    100% {
        opacity: 0.6;
        width: 40%;
        left: 30%;
    }
}

/* FAQ button styling with better hover effect */
.stButton button[data-testid^="stWidgetButton"] {
    background-color: #f8f9fa !important;
    color: #2C3E50 !important;
    border: 1px solid #e0e5eb !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    margin-bottom: 8px;
    text-align: left;
    transition: all 0.15s ease;
}

.stButton button[data-testid^="stWidgetButton"]:hover {
    background-color: #EFF3FF !important;
    color: #4169E1 !important;
    border-color: #4169E1 !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(65,105,225,0.15) !important;
}

.stButton button[data-testid^="stWidgetButton"]:active {
    background-color: #4169E1 !important;
    color: white !important;
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(65,105,225,0.2) !important;
    transition: all 0.05s ease-out;
}

/* Remove focus outlines */
button:focus, button:active {
    outline: none !important;
    box-shadow: none !important;
}

/* Upload button styling */
.upload-btn-container {
    margin-top: 20px;
    margin-bottom: 20px;
}

/* Loading animation improvement */
.stSpinner {
    border-width: 3px !important;
    animation: spinner-border 0.75s linear infinite !important;
}

/* Smooth scroll behavior */
html {
    scroll-behavior: smooth;
}

/* Fade in animation for page load */
@keyframes fadeInPage {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

.main {
    animation: fadeInPage 0.8s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

# App header with improved styling
st.markdown(
    "<h1 class='main-header'>🛡️ Insurance Advisor Chatbot</h1>",
    unsafe_allow_html=True)

# Sidebar for document management
with st.sidebar:
    st.header("Document Management")
    
    # Toggle for showing/hiding document upload
    if st.button("Upload Insurance Policy Document", key="toggle_upload"):
        st.session_state.show_document_upload = not st.session_state.show_document_upload
    
    # Only show document upload if toggled on
    if st.session_state.show_document_upload:
        handle_document_upload()
    
    # Document switcher (only show if documents are available)
    if st.session_state.documents and len(st.session_state.documents) > 1:
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
            else:
                # Create knowledge base from the custom document
                kb = create_knowledge_base(custom_pdf_path=st.session_state.
                                           documents[selected_document])
            
            # Initialize chatbot with the selected knowledge base
            st.session_state.chatbot = InsuranceChatbot(kb)
            st.session_state.active_document = selected_document
            st.session_state.chat_history = []  # Reset chat history when switching documents
            st.rerun()
    
    # About section
    st.markdown("---")
    st.markdown("""
    ### About this Chatbot
    
    This AI assistant helps you understand insurance policies by providing accurate information from insurance documents. The chatbot uses Google's Gemini model and LangChain to process and retrieve relevant information.
    
    **Features:**
    - Answers questions about insurance policies
    - References actual insurance policy documents
    - Suggests human assistance when needed
    """)

# Main chat container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Welcome message when no chat history
if not st.session_state.chat_history:
    st.markdown("""
    ### Welcome to the Insurance Assistant!
    
    I can help you understand:
    - Health insurance policies
    - Life insurance plans
    - Auto insurance coverage
    - Home insurance details
    - Policy terms and conditions
    - Claims processes
    
    Ask me any insurance-related question to get started!
    """)

# Display chat history with feedback buttons
display_chat_history(st.session_state.chat_history)

st.markdown("</div>", unsafe_allow_html=True)  # Close the chat container


# Function to handle user message submission
def submit():
    if "temp_input" in st.session_state and st.session_state.temp_input:
        user_message = st.session_state.temp_input
        temp_value = st.session_state.temp_input
        
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
                # Log the error for debugging
                import traceback
                print(f"Error in submit: {str(e)}")
                print(traceback.format_exc())
                
                # Add a more user-friendly error message
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": "I apologize, but I'm having trouble processing your question. Let me connect you with a customer support executive who can help you better."
                })
        
        # Use a placeholder to store the input temporarily and clear on rerun
        if "clear_input" not in st.session_state:
            st.session_state.clear_input = True
        
        st.rerun()


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
            # Log the error for debugging
            import traceback
            print(f"Error in process_faq: {str(e)}")
            print(traceback.format_exc())
            
            # Add a more user-friendly error message
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "I apologize, but I'm having trouble processing your question. Let me connect you with a customer support executive who can help you better."
            })
    
    st.rerun()


# Modern chat input area
with st.container():
    # Initialize temp_input if it doesn't exist
    if "temp_input" not in st.session_state:
        st.session_state.temp_input = ""
    
    # Text input with improved styling
    st.text_input("Type your insurance question here...",
                  key="temp_input",
                  on_change=submit,
                  placeholder="Example: What does auto insurance typically cover?")
    
    col1, col2 = st.columns([5, 1])
    with col1:
        if st.button("Send", use_container_width=True):
            submit()
    
    with col2:
        if st.button("Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # FAQ section with improved design
    st.markdown("### Quick Questions")
    faq_questions = [
        "What are the eligibility criteria for life insurance?",
        "How do I file a health insurance claim?",
        "What does auto liability insurance cover?",
        "What factors affect my home insurance premium?",
        "What is the difference between term and whole life insurance?",
        "How much coverage do I need for my car insurance?"
    ]
    
    # Display FAQ questions with better styling
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
    "*This chatbot uses AI to provide information about insurance policies based on our knowledge base. For complex inquiries or specific policy details, please contact our customer service.*"
)