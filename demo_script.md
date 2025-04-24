# Insurance Chatbot Demo Script

## Introduction (30 seconds)

*[Show the chatbot interface with the main screen visible]*

**Voiceover:** "Welcome to the Insurance Advisor Chatbot demonstration. This AI-powered assistant helps users understand complex insurance information through a natural conversation interface. Built using Google's Gemini model, LangChain, and FAISS vector database, it provides accurate responses from insurance policy documents while maintaining a human-like conversation flow."

## System Architecture (45 seconds)

*[Display a simple diagram showing the components: UI → Vector DB → LLM]*

**Voiceover:** "The system architecture combines several cutting-edge technologies. Insurance documents are processed and stored in a FAISS vector database, which enables semantic search beyond simple keyword matching. When a user asks a question, the system finds the most relevant information from the knowledge base and uses Google's Gemini model to generate a natural, accurate response. LangChain orchestrates this entire process while maintaining conversation context for follow-up questions."

## Basic Interaction Demo (60 seconds)

*[Show yourself typing a question and receiving a response]*

**Voiceover:** "Let's ask a basic insurance question. I'll type 'What is the difference between term and whole life insurance?' Notice how the system quickly retrieves the relevant information and responds with a clear, concise explanation that distinguishes between these two policy types. The response is factually accurate and uses easy-to-understand language while maintaining a conversational tone."

*[Show the response appearing with typing animation]*

**Voiceover:** "The response appears with a natural typing animation to create a more human-like interaction. This helps users follow along with the information being presented."

## UI Features (45 seconds)

*[Navigate through different UI elements]*

**Voiceover:** "The user interface features a modern, clean design with subtle animations. The chat container has an animated gradient border that creates visual interest without being distracting. Message bubbles use a gentle fade-in effect, and the typing animation mimics human response patterns."

*[Show the quick question buttons]*

**Voiceover:** "For common insurance questions, users can simply click these predefined options instead of typing. This accelerates the information-finding process for frequently asked questions."

*[Show the feedback buttons]*

**Voiceover:** "After each response, users can provide feedback using these thumbs up or down buttons. This helps continuously improve the system's performance over time."

## Knowledge Base Management (60 seconds)

*[Open the sidebar and show the document management section]*

**Voiceover:** "The system comes pre-loaded with sample insurance policy information, but its real power lies in customization. By clicking this button in the sidebar, users can upload their own insurance policy documents in PDF format."

*[Show uploading a document]*

**Voiceover:** "When a document is uploaded, the system automatically extracts the text, splits it into appropriate chunks, converts it to vector embeddings, and adds it to the searchable knowledge base. From that point on, the chatbot can answer questions based on the newly uploaded document."

*[Show document switching if multiple are available]*

**Voiceover:** "If multiple documents are uploaded, users can switch between them using this dropdown menu, allowing for targeted questions about specific policies."

## Complex Query Handling (60 seconds)

*[Type a more complex multi-part question]*

**Voiceover:** "Let's try a more complex question: 'What factors affect my home insurance premium and how can I lower my costs?' This requires understanding multiple concepts and synthesizing information from different sections of the knowledge base."

*[Show the response]*

**Voiceover:** "Notice how the system provides a comprehensive answer, first explaining the various factors that affect premiums, then offering specific strategies for cost reduction. The information is organized logically and presented in a way that's easy to understand."

## Fallback Mechanism (45 seconds)

*[Type a question outside the knowledge base or too specific]*

**Voiceover:** "Now, let's ask something that might be beyond the system's knowledge: 'Can you give me a quote for my specific situation?' The chatbot recognizes that this requires personalized information it doesn't have access to."

*[Show the escalation response]*

**Voiceover:** "Instead of providing incorrect information, the system acknowledges its limitations and offers to connect the user with a human agent who can handle this specific request. This appropriate escalation ensures users always receive accurate help, even for complex cases."

## Technical Highlights (45 seconds)

*[Show code snippets or system components]*

**Voiceover:** "Behind the scenes, several technical innovations make this possible. The vector database enables semantic search that understands the meaning behind words, not just matching keywords. LangChain's retrieval augmented generation combines the knowledge base with the language model's capabilities. Careful prompt engineering ensures responses are factual and helpful."

*[Show the system responding to a follow-up question]*

**Voiceover:** "The system also maintains conversation context, allowing for natural follow-up questions without repeating all the details."

## Implementation Benefits (30 seconds)

**Voiceover:** "This implementation offers several key advantages. It's built on open-source components that can run locally or in the cloud. The knowledge base can be continuously updated as policies change. The modular architecture allows for easy upgrades as AI technology improves. And most importantly, it provides immediate, accurate information to users without requiring specialized insurance knowledge."

## Conclusion (30 seconds)

*[Return to the main chatbot interface]*

**Voiceover:** "The Insurance Advisor Chatbot demonstrates how modern AI technologies can transform complex information access. By combining vector databases, large language models, and thoughtful user experience design, we've created a system that makes insurance information more accessible and understandable. Thank you for watching this demonstration of our insurance chatbot solution."

## Technical Setup Notes (Not for Voiceover)

1. **Environment Preparation:**
   - Ensure all dependencies are installed (see requirements.txt)
   - Set up the Google API key in a .env file
   - Run the application with `streamlit run app.py`

2. **Demo Flow:**
   - Start with a clean chat history
   - Prepare sample questions in advance
   - Have a sample PDF ready for upload demonstration
   - Test all features before recording

3. **Recording Tips:**
   - Use screen recording software with audio input
   - Consider recording the voiceover separately if needed
   - Maintain a steady pace, not too fast or slow
   - Practice the full demo a few times before recording

4. **Key Points to Emphasize:**
   - Accuracy of information
   - Natural conversational flow
   - Modern user interface
   - Proper handling of limitations
   - Customizability with different documents

5. **Potential Questions to Demonstrate:**
   - "What is the difference between HMO and PPO health plans?"
   - "How do I file an auto insurance claim?"
   - "What factors affect my home insurance premium?"
   - "What does liability coverage include?"
   - "Are pre-existing conditions covered under health insurance?"
   - "What is the process for applying for life insurance?"