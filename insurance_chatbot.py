import os
from typing import List, Dict, Any
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

class InsuranceChatbot:
    def __init__(self, knowledge_base):
        """
        Initialize the insurance chatbot with a knowledge base.

        Args:
            knowledge_base: Vector database with insurance policy information
        """
        self.knowledge_base = knowledge_base
        self.api_key = os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")

        # Initialize the Gemini chat model
        try:
            # Configure Gemini API
            genai.configure(api_key=self.api_key)

            # Get available models to debug
            models = genai.list_models()
            print("Available Gemini models:", [model.name for model in models])

            # Use a specific model to avoid compatibility issues
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-latest", # Use the correct model name
                temperature=0.3,
                google_api_key=self.api_key
            )
        except Exception as e:
            print(f"Error initializing Gemini model: {str(e)}")
            raise

        # Set up conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="question",
            output_key="answer"
        )

        # Create the QA template
        qa_template = """
        You are an expert insurance advisor chatbot. Your job is to provide accurate, helpful information 
        about insurance policies including health, life, auto, and home insurance.

        Use the following context to answer the user's question. If you don't know the answer, don't make up 
        information - instead, suggest that the user should contact a human agent for more specific details.

        Remember to be professional, friendly, and clear in your responses.

        Context: {context}

        Question: {question}

        Chat History: {chat_history}

        Answer:
        """

        QA_PROMPT = PromptTemplate(
            template=qa_template, 
            input_variables=["context", "question", "chat_history"]
        )

        # Set up the conversational retrieval chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.knowledge_base.as_retriever(search_kwargs={"k": 4}),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": QA_PROMPT},
            return_source_documents=True,
            verbose=True,
            output_key="answer"  # Specify which output key to store in memory
        )

    def get_response(self, query: str) -> str:
        """
        Get a response from the chatbot for a given query.

        Args:
            query: The user's question about insurance

        Returns:
            A response string with information about the insurance query
        """
        try:
            # Check if the query is about insurance
            if not self._is_insurance_related(query):
                return (
                    "I'm an insurance specialist and can only answer questions related to insurance policies, "
                    "coverage, premiums, and claims. Could you please ask an insurance-related question?"
                )

            print(f"Processing query: {query}")

            # Get response from the conversation chain
            result = self.chain({"question": query})

            print(f"Got result: {result.keys()}")

            # Check if we need to escalate to a human agent
            if self._should_escalate(query, result['answer']):
                return (
                    f"{result['answer']}\n\n"
                    "For this specific query, it might be better to speak with one of our human insurance agents. "
                    "Would you like me to arrange for someone to contact you?"
                )

            return result['answer']

        except Exception as e:
            # Detailed error logging for debugging
            print(f"Error in get_response: {type(e).__name__}: {str(e)}")
            import traceback
            print(traceback.format_exc())

            # Fallback error handling with more specific information
            return (
                f"I'm having trouble processing your request at the moment. "
                f"This could be due to technical difficulties or the complexity of your query. "
                f"Error type: {type(e).__name__}. "
                f"Please try again or consider speaking with one of our human insurance agents for assistance."
            )

    def _is_insurance_related(self, query: str) -> bool:
        """
        Check if the query is related to insurance.

        Args:
            query: The user query

        Returns:
            Boolean indicating if the query is insurance-related
        """
        insurance_keywords = [
            "insurance", "policy", "premium", "coverage", "claim", "deductible",
            "health", "life", "auto", "car", "home", "property", "liability",
            "medical", "accident", "damage", "injury", "protection", "risk",
            "benefit", "plan", "term", "whole life", "comprehensive", "collision"
        ]

        query_lower = query.lower()
        return any(keyword in query_lower for keyword in insurance_keywords)

    def _should_escalate(self, query: str, answer: str) -> bool:
        """
        Determine if a query should be escalated to a human agent.

        Args:
            query: The user query
            answer: The generated answer

        Returns:
            Boolean indicating if the query should be escalated
        """
        # Check for complex cases that might need human intervention
        complex_indicators = [
            "I don't have enough information",
            "I cannot provide",
            "would need more details",
            "cannot accurately",
            "specific to your situation",
            "recommend speaking with an agent",
            "cannot calculate",
            "varies depending on"
        ]

        # Check for specific complex topics
        complex_topics = [
            "lawsuit", "legal", "sue", "death", "dispute", "rejected claim",
            "denied", "appeal", "fraud", "investigation", "cancelation",
            "specific quote", "exact premium", "exact rate", "specific to my case"
        ]

        # If the answer indicates uncertainty or the query is about complex topics
        query_lower = query.lower()
        return (
            any(indicator in answer for indicator in complex_indicators) or
            any(topic in query_lower for topic in complex_topics)
        )
