import os
from typing import List, Dict, Any
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
            logger.info(f"Available Gemini models: {[model.name for model in models]}")

            # Use a specific model (using the latest available)
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-latest",  # Use a modern model
                temperature=0.2,  # Lower temperature for more factual responses
                google_api_key=self.api_key,
                convert_system_message_to_human=True
            )
        except Exception as e:
            logger.error(f"Error initializing Gemini model: {str(e)}")
            raise

        # Set up conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="question",
            output_key="answer"
        )

        # Create the system prompt template
        system_template = """
        You are InsuranceGPT, an expert insurance advisor chatbot designed to provide accurate, helpful, and professional insurance information. 
        
        RULES:
        1. Only answer questions based on the information provided in the context
        2. If the information isn't in the context, politely inform the user and suggest contacting a human agent
        3. Never make up information or hallucinate facts about insurance
        4. Be professional but conversational, using clear and simple language without insurance jargon
        5. When explaining complex insurance terms, break them down simply
        6. Provide concise, well-structured responses
        
        When users ask about specific policies or premiums, remind them that:
        - The information provided is general and their actual policy details may vary
        - For specific quotes or policy changes, they should contact an insurance representative
        
        CONTEXT INFORMATION:
        {context}
        
        PREVIOUS CONVERSATION:
        {chat_history}
        
        CURRENT QUESTION: {question}
        
        YOUR RESPONSE:
        """

        QA_PROMPT = PromptTemplate(
            template=system_template, 
            input_variables=["context", "question", "chat_history"]
        )

        # Set up the conversational retrieval chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.knowledge_base.as_retriever(
                search_kwargs={"k": 4},  # Retrieve 4 most relevant chunks
                search_type="similarity"  # Use similarity search
            ),
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

            logger.info(f"Processing query: {query}")

            # Get response from the conversation chain
            result = self.chain({"question": query})

            logger.info(f"Got result: {result.keys()}")

            # Get source documents for citation
            source_docs = result.get('source_documents', [])
            
            # Format source information if available
            source_info = ""
            if source_docs:
                source_names = set()
                for doc in source_docs:
                    if 'source' in doc.metadata:
                        source_name = doc.metadata['source'].split('/')[-1]
                        source_names.add(source_name)
                
                if source_names:
                    source_info = "\n\n*Information sourced from: " + ", ".join(source_names) + "*"

            # Check if we need to escalate to a human agent
            if self._should_escalate(query, result['answer']):
                return (
                    f"{result['answer']}\n\n"
                    "For this specific query, it might be better to speak with one of our human insurance agents. "
                    "Would you like me to arrange for someone to contact you?" + source_info
                )

            return result['answer'] + source_info

        except Exception as e:
            # Detailed error logging for debugging
            logger.error(f"Error in get_response: {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

            # Fallback error handling with more specific information
            return (
                f"I'm having trouble processing your request at the moment. "
                f"This could be due to technical difficulties or the complexity of your query. "
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
            "benefit", "plan", "term", "whole life", "comprehensive", "collision",
            "policyholder", "insurer", "insured", "beneficiary", "underwriting", 
            "copay", "coinsurance", "out-of-pocket", "preexisting", "coverage limit"
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
            "varies depending on",
            "I don't have specific information",
            "I cannot access",
            "not available in the provided context"
        ]

        # Check for specific complex topics
        complex_topics = [
            "lawsuit", "legal", "sue", "death", "dispute", "rejected claim",
            "denied", "appeal", "fraud", "investigation", "cancelation",
            "specific quote", "exact premium", "exact rate", "specific to my case",
            "personal information", "policy number", "payment information"
        ]

        # If the answer indicates uncertainty or the query is about complex topics
        query_lower = query.lower()
        return (
            any(indicator.lower() in answer.lower() for indicator in complex_indicators) or
            any(topic in query_lower for topic in complex_topics)
        )