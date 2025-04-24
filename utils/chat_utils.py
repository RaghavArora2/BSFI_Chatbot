import os
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Generator, List, Dict, Optional
import google.generativeai as genai
import streamlit as st
from utils.prompt_templates import (
    INSURANCE_ASSISTANT_PROMPT,
    FALLBACK_PROMPT,
    POLICY_SUMMARY_PROMPT,
    POLICY_COMPARISON_PROMPT,
    TERM_EXPLANATION_PROMPT
)

# Configure Google Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    # If API key is not set, warn but continue for development purposes
    print("Warning: GOOGLE_API_KEY not set in environment variables")

def format_chat_history(messages: List[Dict]) -> List:
    """
    Convert chat history to LangChain format.
    
    Args:
        messages (List[Dict]): List of message dictionaries with 'role' and 'content'
        
    Returns:
        List: Chat history in LangChain format
    """
    formatted_messages = []
    
    for message in messages:
        if message["role"] == "user":
            formatted_messages.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            formatted_messages.append(AIMessage(content=message["content"]))
    
    return formatted_messages

def get_relevant_context(query: str, vector_store, max_docs: int = 5) -> str:
    """
    Retrieve relevant context from the vector store based on the query.
    
    Args:
        query (str): User query
        vector_store: FAISS vector store
        max_docs (int): Maximum number of documents to retrieve
        
    Returns:
        str: Relevant context from the knowledge base
    """
    try:
        # Enhance the query for better search results
        enhanced_query = enhance_search_query(query)
        
        # Search for the most relevant documents
        results = vector_store.similarity_search(
            enhanced_query,
            k=max_docs  # Number of documents to retrieve
        )
        
        # Combine the content of relevant documents
        context = "\n\n".join([doc.page_content for doc in results])
        return context
    except Exception as e:
        print(f"Error retrieving context: {str(e)}")
        return ""

def enhance_search_query(query: str) -> str:
    """
    Enhance the search query to improve retrieval performance.
    
    Args:
        query (str): Original user query
        
    Returns:
        str: Enhanced query
    """
    # Convert to lowercase for consistent matching
    query = query.lower()
    
    # Dictionary of insurance terms and their related terms for expansion
    insurance_terms = {
        "car": ["auto", "vehicle", "automobile"],
        "auto": ["car", "vehicle", "automobile"],
        "health": ["medical", "healthcare", "wellness"],
        "home": ["house", "property", "dwelling", "homeowner"],
        "life": ["death benefit", "term life", "whole life"],
        "premium": ["cost", "payment", "fee", "price"],
        "deductible": ["out-of-pocket", "expense"],
        "claim": ["filing claim", "claim process", "submit claim"],
        "coverage": ["protection", "insure against", "policy covers"]
    }
    
    # Expand query with related terms
    expanded_terms = []
    for term, related in insurance_terms.items():
        if term in query:
            expanded_terms.extend(related)
    
    # Combine original query with expanded terms
    if expanded_terms:
        enhanced_query = f"{query} {' '.join(expanded_terms)}"
        return enhanced_query
    
    return query

def detect_query_intent(query: str) -> Optional[str]:
    """
    Detect the intent of the user's query to use specialized prompts.
    
    Args:
        query (str): User query
        
    Returns:
        Optional[str]: Detected intent or None
    """
    query_lower = query.lower()
    
    # Check for policy comparison intent
    if any(term in query_lower for term in ["compare", "difference between", "versus", "vs"]):
        if sum(1 for policy_type in ["auto", "car", "health", "home", "life"] if policy_type in query_lower) >= 2:
            return "comparison"
    
    # Check for policy summary intent
    if any(term in query_lower for term in ["summary", "overview", "brief", "what is"]):
        for policy_type in ["auto insurance", "car insurance", "health insurance", "home insurance", "life insurance"]:
            if policy_type in query_lower:
                return f"summary:{policy_type}"
    
    # Check for term explanation intent
    if any(term in query_lower for term in ["what is a", "what does", "mean", "define", "explanation"]):
        for term in ["premium", "deductible", "claim", "coverage", "policy", "rider"]:
            if term in query_lower:
                return f"term_explanation:{term}"
    
    # Default to general query
    return None

def select_prompt_template(query: str, intent: Optional[str], context: str) -> str:
    """
    Select the appropriate prompt template based on query intent.
    
    Args:
        query (str): User query
        intent (Optional[str]): Detected intent
        context (str): Retrieved context
        
    Returns:
        str: Formatted prompt
    """
    if not intent:
        # Use default insurance assistant prompt
        return PromptTemplate.from_template(INSURANCE_ASSISTANT_PROMPT).format(
            context=context,
            question=query
        )
    
    if intent == "comparison":
        # Extract policy types for comparison
        policy_types = []
        for policy_type in ["auto", "car", "health", "home", "life"]:
            if policy_type in query.lower():
                policy_types.append(policy_type)
        
        policy_types_str = ", ".join(policy_types)
        return PromptTemplate.from_template(POLICY_COMPARISON_PROMPT).format(
            context=context,
            policy_types=policy_types_str
        )
    
    if intent.startswith("summary:"):
        policy_type = intent.split(":", 1)[1]
        return PromptTemplate.from_template(POLICY_SUMMARY_PROMPT).format(
            context=context,
            policy_type=policy_type
        )
    
    if intent.startswith("term_explanation:"):
        term = intent.split(":", 1)[1]
        return PromptTemplate.from_template(TERM_EXPLANATION_PROMPT).format(
            context=context,
            term=term
        )
    
    # Fallback to default prompt
    return PromptTemplate.from_template(INSURANCE_ASSISTANT_PROMPT).format(
        context=context,
        question=query
    )

def get_gemini_response(query: str, vector_store, chat_history: List[Dict]) -> Generator[str, None, None]:
    """
    Get a response from Google Gemini with relevant context.
    
    Args:
        query (str): User query
        vector_store: FAISS vector store
        chat_history (List[Dict]): Previous chat messages
        
    Returns:
        Generator[str, None, None]: Generator yielding response chunks
    """
    try:
        # Get relevant context from the vector store
        context = get_relevant_context(query, vector_store)
        
        # Detect query intent for specialized handling
        intent = detect_query_intent(query)
        
        # Select appropriate prompt template based on intent
        formatted_prompt = select_prompt_template(query, intent, context)
        
        # Initialize Gemini model with appropriate parameters
        model = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.3,  # Lower temperature for more factual responses
            convert_system_message_to_human=True,
            streaming=True,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
            ]
        )
        
        # Format chat history for LangChain
        formatted_history = format_chat_history(chat_history[-5:])  # Use last 5 messages for context
        
        # Add a system message to the front of the history if not present
        system_message = SystemMessage(content="You are an AI assistant for an insurance company that provides clear, concise, and accurate information about insurance policies, coverage options, and claims processes.")
        history_with_system = [system_message] + formatted_history
        
        # Generate response
        response = model.stream(
            formatted_prompt,
            history_with_system
        )
        
        # Yield each chunk of the response
        for chunk in response:
            if hasattr(chunk, 'content'):
                yield chunk.content
            elif isinstance(chunk, str):
                yield chunk
            else:
                yield str(chunk)
                
    except Exception as e:
        error_message = f"I'm sorry, I encountered an error: {str(e)}. Please try again or contact customer support."
        yield error_message
