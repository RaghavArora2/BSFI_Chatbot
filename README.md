# Insurance Advisor Chatbot


A sophisticated AI-powered insurance policy chatbot built with **Streamlit** and **Google Gemini**, designed to provide intelligent customer support through a modern conversational interface.

## Foundational Architecture

The insurance chatbot employs a multi-layered architecture that integrates several advanced AI and data management technologies:

### 1. **Vector Knowledge Base**

The knowledge base layer serves as the foundation of the system, storing and retrieving information from insurance policy documents. Key components include:

- **Document Processing Pipeline:**
  - **Text Extraction:** PDFs and text files undergo extraction using **PyPDFLoader** and **TextLoader**.
  - **Chunking:** Documents are divided into semantically coherent segments using **RecursiveCharacterTextSplitter** with carefully calibrated chunk size (1000 characters) and overlap (200 characters) parameters to preserve context while optimizing retrieval.
  - **Embeddings Generation:** Text chunks are transformed into high-dimensional vector representations using **Google's embedding model**.
  - **Vector Indexing:** **FAISS** (Facebook AI Similarity Search) creates an efficient similarity-searchable index of these embeddings.

This approach enables semantic understanding beyond simple keyword matching, allowing the system to comprehend the intent and meaning behind user queries and retrieve the most relevant information.

### 2. **Language Model Integration**

The chatbot utilizes **Google's Gemini model** for natural language understanding and response generation:

- **Model Configuration:**
  - **Selected Model:** `gemini-1.5-flash-latest` provides an optimal balance of response quality and latency.
  - **Temperature Setting:** Set to `0.2` to ensure deterministic, factually grounded responses while maintaining natural language flow.
  - **System Prompting:** Carefully crafted prompt engineering constrains the model to:
    - Only respond based on retrieved knowledge.
    - Maintain a professional but conversational tone.
    - Simplify complex insurance terminology.
    - Avoid hallucinating information not present in the source documents.
    - Escalate appropriately when human expertise is required.

### 3. **Conversational Framework**

**LangChain** provides the orchestration layer connecting the vector database with the language model and managing conversational state:

- **Key Components:**
  - **ConversationalRetrievalChain:** Coordinates the workflow between query processing, retrieval, and response generation.
  - **ConversationBufferMemory:** Maintains chat history to provide context for multi-turn dialogues.
  - **PromptTemplate:** Structures inputs to the model with context, user query, and conversation history.

### 4. **User Interface**

The **Streamlit**-based interface delivers a modern, responsive user experience:

- **UI Features:**
  - **Animated Elements:** Subtle animations including gradient borders and typing effects enhance engagement.
  - **Accessibility:** Clean layout with appropriate contrast and sizing for diverse users.
  - **Responsive Design:** Adapts to different screen sizes and orientations.
  - **Feedback Mechanisms:** Integrated rating system for continuous improvement.

### Local Installation

1. **Clone the repository**

```bash
git clone https://github.com/RaghavArora2/BSFI_Chatbot.git
```

2. **Set up a virtual environment (recommended)**

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Edit API key in app.py:

```
GOOGLE_API_KEY=your_google_api_key_here
```

5. **Run the application**

```bash
streamlit run app.py
`````

## 📖 Usage Guide

### Asking Questions

Simply type your insurance-related questions in the chat input and press Enter. Example questions:

- "What is the difference between term and whole life insurance?"
- "How do deductibles work in health insurance?"
- "What factors affect my home insurance premium?"
- "When should I file an auto insurance claim?"

### Uploading Documents

1. Click on the sidebar expander
2. Upload your insurance policy PDF
3. Wait for processing to complete
4. Your questions will now include information from your document

### Quick Questions

Click on the pre-defined question buttons for instant answers to common insurance queries.

