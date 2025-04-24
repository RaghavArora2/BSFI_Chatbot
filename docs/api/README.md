# Insurance Chatbot API Reference

This document provides technical information about the key modules and functions in the Insurance Advisor Chatbot.

## Table of Contents

1. [app.py](#apppy)
2. [insurance_chatbot.py](#insurance_chatbotpy)
3. [knowledge_base.py](#knowledge_basepy)
4. [utils.py](#utilspy)

## app.py

The main Streamlit application that serves as the user interface.

### Key Functions

#### `handle_document_upload()`

Handles the uploading and processing of PDF documents.

```python
def handle_document_upload():
    # Uploads and processes PDF documents to create a knowledge base
    # Returns: None
```

#### `submit()`

Processes user input and gets a response from the chatbot.

```python
def submit():
    # Processes the user's question and retrieves a response
    # Returns: None
```

#### `process_faq(question)`

Processes predefined FAQ questions.

```python
def process_faq(question):
    # Parameters:
    #   question (str): The FAQ question text
    # Returns: None
```

## insurance_chatbot.py

Core chatbot logic including LLM integration and response generation.

### Classes

#### `InsuranceChatbot`

The main chatbot class that handles NLP tasks.

```python
class InsuranceChatbot:
    def __init__(self, knowledge_base):
        # Parameters:
        #   knowledge_base: Vector database with insurance policy information
```

#### Key Methods

##### `get_response(query: str) -> str`

Gets a response from the chatbot for a given query.

```python
def get_response(self, query: str) -> str:
    # Parameters:
    #   query (str): The user's question about insurance
    # Returns:
    #   str: A response string with information about the insurance query
```

##### `_is_insurance_related(query: str) -> bool`

Checks if the query is related to insurance.

```python
def _is_insurance_related(self, query: str) -> bool:
    # Parameters:
    #   query (str): The user query
    # Returns:
    #   bool: True if the query is insurance-related
```

##### `_is_no_information_response(answer: str) -> bool`

Determines if the response indicates that no information was found.

```python
def _is_no_information_response(self, answer: str) -> bool:
    # Parameters:
    #   answer (str): The generated answer
    # Returns:
    #   bool: True if the answer indicates lack of information
```

##### `_should_escalate(query: str, answer: str) -> bool`

Determines if a query should be escalated to a human agent.

```python
def _should_escalate(self, query: str, answer: str) -> bool:
    # Parameters:
    #   query (str): The user query
    #   answer (str): The generated answer
    # Returns:
    #   bool: True if the query should be escalated
```

## knowledge_base.py

Handles document processing and vector database creation.

### Key Functions

#### `create_knowledge_base(custom_pdf_path=None, custom_text=None)`

Creates a knowledge base from insurance policy documents or custom text.

```python
def create_knowledge_base(custom_pdf_path=None, custom_text=None):
    # Parameters:
    #   custom_pdf_path (str, optional): Path to a custom PDF document
    #   custom_text (str, optional): Custom text to use instead of documents
    # Returns:
    #   vector_store: A FAISS vector store containing insurance policy information
```

#### `create_sample_insurance_files(directory_path)`

Creates sample insurance policy files in the specified directory.

```python
def create_sample_insurance_files(directory_path):
    # Parameters:
    #   directory_path (str): The directory where to create sample files
    # Returns:
    #   None
```

#### `create_fallback_document()`

Creates a fallback document when no other sources are available.

```python
def create_fallback_document():
    # Returns:
    #   str: Text content for a fallback insurance document
```

## utils.py

Helper functions for UI and chat functionality.

### Key Functions

#### `display_chat_history(chat_history: List[Dict[str, Any]])`

Displays the chat history in the UI with a typing animation effect.

```python
def display_chat_history(chat_history: List[Dict[str, Any]]):
    # Parameters:
    #   chat_history: List of message dictionaries with 'role' and 'content' keys
    # Returns:
    #   None
```

#### `give_feedback(msg_idx, feedback_type)`

Processes user feedback on chatbot responses.

```python
def give_feedback(msg_idx, feedback_type):
    # Parameters:
    #   msg_idx: Index of the message in chat history
    #   feedback_type: Type of feedback ("positive" or "negative")
    # Returns:
    #   None
```

## Working with Environment Variables

The application uses the following environment variables:

1. `GOOGLE_API_KEY`: (Required) Your Google API key for Gemini
2. `PORT`: (Optional) Port to run the Streamlit server
3. `LOGGING_LEVEL`: (Optional) Set logging verbosity
4. `MODEL_NAME`: (Optional) Specific Gemini model to use
5. `TEMPERATURE`: (Optional) Response randomness (0.0-1.0)

These can be set in a `.env` file in the project root.

## Extending the Chatbot

### Adding New Document Types

To add support for new document types:

1. Implement a new loader in `knowledge_base.py`
2. Add the appropriate import
3. Update the logic in `create_knowledge_base()`

Example for adding DOCX support:

```python
from langchain_community.document_loaders import DocxLoader

# In create_knowledge_base()
if custom_docx_path:
    loader = DocxLoader(custom_docx_path)
    documents.extend(loader.load())
```

### Changing the LLM Provider

To switch to a different LLM:

1. Update the imports in `insurance_chatbot.py`
2. Modify the model initialization in `__init__()`
3. Update environment variable handling

Example for switching to OpenAI:

```python
from langchain_openai import ChatOpenAI

# In __init__()
self.llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.2,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
```

### Customizing the UI

The UI styling is defined in the CSS section of `app.py`. You can modify it by:

1. Locating the `st.markdown("""<style>...""")` section
2. Editing the CSS rules
3. Adding new styles as needed

Example for changing the primary color:

```css
/* Change primary color from blue to green */
.main-header {
    color: #2E8B57; /* Sea green instead of royal blue */
}

.stButton button {
    background-color: #2E8B57;
}

.assistant-message {
    border-left: 4px solid #2E8B57;
}
```