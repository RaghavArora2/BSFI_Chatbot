# Insurance Chatbot: Complete User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [User Interface Overview](#user-interface-overview)
4. [Using the Chatbot](#using-the-chatbot)
5. [Knowledge Base Management](#knowledge-base-management)
6. [Advanced Configuration](#advanced-configuration)
7. [Troubleshooting](#troubleshooting)
8. [Developer Guide](#developer-guide)

## Introduction

The Insurance Advisor Chatbot is an AI-powered assistant designed to provide accurate information about insurance policies directly from your knowledge base. The system uses advanced vector embeddings, Google's Gemini language model, and LangChain to deliver a natural conversational experience while ensuring factual accuracy.

### Key Features

- **Modern, Animated UI**: Elegant interface with subtle animations for an engaging user experience
- **Semantic Search**: Vector-based retrieval finds the most relevant information even when queries use different terminology
- **Natural Conversations**: Maintains context across multiple questions for coherent dialogue
- **Escalation Mechanism**: Recognizes when a query requires human expertise and offers to connect users with support staff
- **Custom Knowledge Base**: Upload your own insurance policy PDFs to create a customized information source
- **Typing Animation**: Responses appear with a natural typing effect for a more human-like interaction
- **User Feedback**: Thumbs up/down buttons allow users to rate the quality of responses

## Getting Started

### System Requirements

- Python 3.10 or later
- 2GB+ RAM (4GB+ recommended for larger knowledge bases)
- Internet connection (for API access to Google's Gemini model)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd insurance-chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the project root
   - Add your Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```
   - (Optional) Configure additional settings:
     ```
     PORT=5000
     LOGGING_LEVEL=INFO
     ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## User Interface Overview

### Main Components

- **Chat Container**: The central area where conversations appear
- **Input Field**: Text box at the bottom for typing questions
- **Quick Questions**: Pre-defined common insurance queries for one-click answers
- **Sidebar**: Contains document management tools (collapsed by default)
- **Feedback Buttons**: Appear below each chatbot response

### UI Animations

The interface includes several subtle animations to enhance the user experience:

- **Gradient Border**: The chat container features an animated gradient border
- **Message Transitions**: Smooth fade-in and rise effects for new messages
- **Typing Animation**: Chatbot responses appear progressively as if being typed
- **Button Hover Effects**: Interactive elements provide visual feedback on hover
- **Header Pulse**: Subtle animation on the main header title

## Using the Chatbot

### Basic Interaction

1. **Ask a Question**: Type your insurance-related query in the text field at the bottom of the screen
2. **View Response**: The chatbot will analyze your question and provide an answer based on its knowledge base
3. **Follow-up Questions**: The chatbot maintains context, so you can ask follow-up questions without repeating all details
4. **Quick Questions**: Click any of the pre-defined questions for immediate answers to common queries

### Feedback Mechanism

After each chatbot response, you'll see thumbs up/down buttons:

- **Thumbs Up**: Indicates the response was helpful
- **Thumbs Down**: Signals that the response needs improvement
- **Feedback Processing**: The system collects this feedback to improve future responses

### Handling Complex Queries

When a query requires human expertise or contains information not in the knowledge base:

1. The chatbot will acknowledge its limitations
2. It will offer to connect you with a customer support representative
3. You can choose to rephrase your question or proceed with human assistance

## Knowledge Base Management

### Current Knowledge Base

By default, the chatbot comes pre-loaded with sample insurance information covering:

- Health insurance policies
- Life insurance policies
- Auto insurance policies
- Home insurance policies

### Adding New Documents

To expand or customize the knowledge base:

1. **Open the Document Management Panel**: Click the sidebar toggle in the top-left corner
2. **Access Upload Feature**: Click "Upload Insurance Policy Document"
3. **Select Files**: Choose a PDF file containing insurance policy information
4. **Processing**: The system will automatically:
   - Extract text from the PDF
   - Split into appropriate chunks
   - Convert to vector embeddings
   - Add to the searchable knowledge base

### Supported Document Types

- **PDF Documents**: Primary supported format for insurance policies
- **Text Files**: Automatically detected in the attached_assets directory
- **Future Support**: Plans include support for Word documents, HTML, and structured data formats

### Document Switching

If you've uploaded multiple documents:

1. Open the sidebar
2. Go to the "Switch Document" section
3. Select from the dropdown menu to switch between different knowledge sources
4. The chat history will reset when switching documents

### Best Practices for Knowledge Base Documents

For optimal performance when adding your own documents:

1. **Clean Formatting**: Documents with clear headings, sections, and minimal special formatting work best
2. **Searchable Text**: Ensure PDFs contain searchable text, not just scanned images
3. **Document Length**: While any size can work, 5-50 pages per document is ideal for processing
4. **Content Focus**: Documents focused on a specific insurance type or topic perform better than broad, general documents
5. **Text Density**: Documents with concise, information-rich content provide better results than marketing materials with sparse details
6. **Update Frequency**: Regularly update documents to ensure information remains current

## Advanced Configuration

### Environment Variables

The following environment variables can be configured in `.env`:

- `GOOGLE_API_KEY`: (Required) Your Google API key for Gemini access
- `PORT`: (Optional) Port to run the Streamlit server (default: 5000)
- `LOGGING_LEVEL`: (Optional) Set logging verbosity (default: INFO)
- `MODEL_NAME`: (Optional) Specific Gemini model to use (default: gemini-1.5-flash-latest)
- `TEMPERATURE`: (Optional) Response randomness (0.0-1.0, default: 0.2)
- `MAX_TOKENS`: (Optional) Maximum response length (default: 1024)

### Customizing the UI

The UI styling can be customized by modifying the CSS in the `st.markdown` section of `app.py`:

- **Color Scheme**: Change the primary colors (`#4169E1`) to match your brand
- **Animation Speed**: Adjust timing values in animation keyframes
- **Typography**: Modify font settings for headers and body text
- **Layout**: Adjust width, padding, and margin settings

### Model Parameters

Advanced model parameters can be adjusted in `insurance_chatbot.py`:

- **Temperature**: Controls randomness (lower = more deterministic)
- **Top-k Retrieval**: Number of document chunks to retrieve for each query
- **System Prompt**: The instructions that guide the model's response style and constraints

## Troubleshooting

### Common Issues

#### "Failed to connect to Gemini API"
- Check your internet connection
- Verify your API key is correctly set in the environment variables
- Ensure you have access to the selected Gemini model

#### "No relevant information found"
- Your query might be outside the scope of the current knowledge base
- Try rephrasing the question or using different terminology
- Consider uploading additional documents with relevant information

#### "Text extraction failed for uploaded document"
- Ensure the PDF contains searchable text, not just images
- Check the file is not password-protected or encrypted
- Try converting the document using a PDF tool and re-upload

#### "UI appears broken or unresponsive"
- Clear your browser cache
- Try a different browser
- Restart the application

#### "StreamlitDuplicateElementKey Error"
- This rarely happens but can occur after multiple quick interactions
- Simply refresh the page to reset unique element keys
- Avoid rapidly clicking multiple buttons in succession

#### "Double message sending"
- The application has built-in protection against double-sending
- If it still occurs, wait a moment before clicking buttons
- Check network connectivity, as slow connections may trigger resubmissions

#### "Feedback message issues"
- Feedback acknowledgments should appear at the top of the interface
- If missing, try providing feedback again
- In rare cases, clear your browser cache or try a different browser

### Debug Mode

For detailed logging and troubleshooting:

1. Set `LOGGING_LEVEL=DEBUG` in your environment variables
2. Restart the application
3. Check the console for detailed logs of each processing step

## Developer Guide

### Project Structure

```
insurance-chatbot/
├── app.py                  # Main Streamlit application
├── insurance_chatbot.py    # Core chatbot logic and LLM integration
├── knowledge_base.py       # Vector database and document processing
├── utils.py                # Helper functions for UI and feedback
├── .env                    # Environment variables (create this)
├── .env.example            # Example environment configuration
├── requirements.txt        # Python dependencies
├── sample_insurance_policies/  # Default knowledge base documents
└── attached_assets/        # Directory for additional text sources
```

### Key Components

#### 1. Knowledge Base (`knowledge_base.py`)

This component handles:
- Loading documents from PDFs or text files
- Text extraction and preprocessing
- Chunking documents into manageable segments
- Converting text to vector embeddings
- Creating and maintaining the FAISS vector database
- Similarity search for retrieval

To extend or modify the knowledge base implementation:

```python
# Example: Adding a new document loader type
from langchain_community.document_loaders import DocxLoader

# In the create_knowledge_base function
if custom_docx_path:
    loader = DocxLoader(custom_docx_path)
    documents.extend(loader.load())
```

#### 2. Chatbot Core (`insurance_chatbot.py`)

This component:
- Initializes the language model (Google Gemini)
- Sets up the conversational retrieval chain
- Manages conversation context and memory
- Processes user queries and generates responses
- Implements fallback and escalation logic

To customize the model behavior:

```python
# Example: Adjusting model parameters
self.llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",  # Change model version
    temperature=0.3,         # Adjust creativity/randomness
    google_api_key=self.api_key,
    max_tokens=2048          # Increase maximum response length
)
```

#### 3. User Interface (`app.py`)

The UI component:
- Creates the Streamlit web interface
- Manages session state and user interactions
- Handles document uploading and switching
- Applies styling and animations
- Processes user input and displays responses

To modify the UI layout:

```python
# Example: Adding a new section to the interface
with st.expander("Advanced Options", expanded=False):
    st.slider("Response Detail Level", 1, 5, 3, 
              help="Adjust how detailed the responses should be")
```

#### 4. Utilities (`utils.py`)

Contains helper functions for:
- Displaying chat history with proper formatting
- Processing user feedback
- Implementing typing animation effects
- Managing session state

### Extension Points

1. **Adding New Model Providers**:
   Modify `insurance_chatbot.py` to support additional LLM providers (OpenAI, Anthropic, etc.)

2. **Enhanced Analytics**:
   Extend the feedback mechanism to store and analyze user interactions

3. **Multi-modal Support**:
   Implement image processing for insurance documents or photos

4. **Custom Embeddings**:
   Replace the default embeddings with domain-specific insurance embeddings

5. **Authentication Layer**:
   Add user authentication for personalized experiences

### Testing

To run tests:

```bash
pytest tests/
```

Key test areas:
- Knowledge base creation and retrieval accuracy
- Response generation quality and factualness
- UI component functionality
- Fallback mechanism effectiveness

## Conclusion

The Insurance Advisor Chatbot provides a powerful combination of modern UI, advanced AI, and flexible knowledge management. By following this guide, you can effectively deploy, customize, and maintain the system to provide accurate insurance information to your users.

For additional support or feature requests, please contact the development team or open an issue in the project repository.