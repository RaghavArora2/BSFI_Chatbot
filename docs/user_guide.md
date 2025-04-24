# Insurance Advisor Chatbot

![Insurance Advisor](./assets/chatbot-preview.png)

## Overview

The Insurance Advisor Chatbot is an AI-powered assistant that provides accurate information about insurance policies. It uses advanced natural language processing and vector-based retrieval to answer customer questions about various insurance products, coverage details, claims processes, and policy considerations.

Built with Google's Gemini model, LangChain, and FAISS vector database, this chatbot delivers a seamless conversational experience while ensuring responses are factually accurate and grounded in your insurance documentation.

## Features

- 🧠 **AI-Powered Responses**: Leverages Google's Gemini model for natural, accurate answers
- 🔍 **Semantic Search**: Vector-based retrieval finds information even when questions use different terminology
- 📄 **Custom Knowledge Base**: Upload your own insurance policy PDFs
- 💬 **Natural Conversations**: Maintains context across multiple questions
- 🔄 **Animated UI**: Modern interface with smooth transitions and typing effects
- 👍 **User Feedback**: Collect ratings on response quality
- 👤 **Human Escalation**: Automatically identifies when to connect users with support staff

## Quick Installation

### Prerequisites

- Python 3.10+ 
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/insurance-advisor-chatbot.git
cd insurance-advisor-chatbot
```

2. **Set up a virtual environment (recommended)**

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root with the following content:

```
GOOGLE_API_KEY=your_google_api_key_here
```

You can obtain a Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

5. **Run the application**

```bash
streamlit run app.py
```

The chatbot will be available at [http://localhost:8501](http://localhost:8501) in your web browser.

## Usage Guide

### Basic Usage

1. Type your insurance-related question in the text field
2. View the AI-generated response
3. Provide feedback using the thumbs up/down buttons
4. Use the quick question buttons for common insurance queries

### Adding Your Own Knowledge Base

1. Prepare your insurance policy PDFs
2. Click "Upload Insurance Policy Document" in the sidebar
3. Upload your PDF files
4. The system will automatically process and index your documents
5. Start asking questions about your uploaded policies

### Example Questions

- "What is the difference between term and whole life insurance?"
- "How do I file a health insurance claim?"
- "What factors affect my auto insurance premium?"
- "What does liability coverage include for home insurance?"
- "Are pre-existing conditions covered under health insurance?"

## Project Structure

```
insurance-advisor-chatbot/
├── app.py                  # Main Streamlit application
├── insurance_chatbot.py    # Core chatbot logic and LLM integration
├── knowledge_base.py       # Vector database and document processing
├── utils.py                # Helper functions for UI and feedback
├── assets/                 # Images and static files
├── sample_insurance_policies/  # Sample knowledge base documents
├── .env.example            # Example environment configuration
└── requirements.txt        # Python dependencies
```

## Customization

### Changing the UI

The UI styling can be customized by modifying the CSS in `app.py`. Look for the `st.markdown` section that contains the CSS styles.

### Adjusting Model Parameters

You can fine-tune the AI model's behavior by modifying parameters in `insurance_chatbot.py`, such as temperature (randomness), top-k retrieval, and system prompts.

### Adding New Document Types

By default, the system supports PDF documents. You can extend it to support additional formats by modifying `knowledge_base.py`.

## Documentation

For more detailed information, please refer to:

- [User Guide](./docs/user_guide.md): Complete instructions for end users
- [Technical Report](./docs/report.md): Detailed methodology and implementation details
- [API Reference](./docs/api_reference.md): Technical documentation for developers

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini for providing the language model
- LangChain for the framework connecting LLMs with external data
- FAISS for efficient vector similarity search
- Streamlit for the web interface

---

Created by [Your Name] | [Your Website/GitHub](https://github.com/yourusername)