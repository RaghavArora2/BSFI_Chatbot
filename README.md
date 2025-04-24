# Insurance Advisor Chatbot

![Insurance Chatbot Banner](assets/banner.png)

A sophisticated AI-powered insurance policy chatbot built with Streamlit and Google Gemini, designed to provide intelligent customer support through a modern conversational interface.

## 🌟 Features

- **Natural Conversation**: Engage in natural dialogue about insurance policies
- **Smart Knowledge Base**: Utilizes vector database for semantic understanding
- **PDF Document Upload**: Analyze your own insurance documents
- **Modern UI**: Clean interface with animations and smooth transitions
- **Multi-Insurance Support**: Covers health, auto, home, and life insurance
- **Contextual Memory**: Remembers conversation history for follow-up questions
- **Human Fallback**: Gracefully suggests human support when needed

## 🚀 Quick Start

### Online Demo

Try the live demo: [Insurance Advisor Chatbot](https://replit.com/@your-username/insurance-advisor-chatbot)

### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/insurance-advisor-chatbot.git
   cd insurance-advisor-chatbot
   ```

2. Run the setup script:
   ```bash
   python setup.py
   ```

3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Add your Google API key to the `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

6. Open your browser to `http://localhost:8501`

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

### Feedback

After each response, you can provide feedback using the thumbs up/down buttons to help improve the system.

## 🧠 Technology Stack

- **Frontend**: Streamlit (Python-based web app framework)
- **AI/NLP**: Google Gemini (via Google Generative AI API)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Orchestration**: LangChain (Framework for LLM applications)
- **Document Processing**: PyPDF, ReportLab
- **Text Processing**: LangChain document loaders and text splitters

## 📄 Project Structure

```
├── app.py                  # Main Streamlit application
├── insurance_chatbot.py    # Core chatbot logic and LLM integration
├── knowledge_base.py       # Vector database and document processing
├── utils.py                # Helper functions and UI components
├── setup.py                # Installation script
├── sample_insurance_policies/  # Sample insurance documents
├── docs/                   # Documentation
│   ├── api/                # API reference
│   ├── report.md           # Technical report
│   ├── video.md            # Video demo instructions
│   └── answer.md           # Comprehensive methodology
└── assets/                 # Static assets and images
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 Documentation

For more detailed information, please refer to the documentation in the `docs/` directory:

- [Technical Report](docs/report.md): In-depth explanation of methodology and architecture
- [API Reference](docs/api/README.md): Detailed API documentation
- [Video Demo](docs/video.md): Instructions for the demo video
- [Comprehensive Answer](docs/answer.md): Detailed explanation of approach and implementation

## 🛠️ Development

To set up the development environment:

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## 🙏 Acknowledgments

- Google Generative AI for providing the Gemini API
- The LangChain community for their excellent framework
- The Streamlit team for making web app development in Python accessible