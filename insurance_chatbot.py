import os
from typing import List, Dict, Any
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import logging

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

        try:
            genai.configure(api_key=self.api_key)

            models = genai.list_models()
            logger.info(f"Available Gemini models: {[model.name for model in models]}")

            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-latest", 
                temperature=0.2,
                google_api_key=self.api_key,
                convert_system_message_to_human=True
            )
        except Exception as e:
            logger.error(f"Error initializing Gemini model: {str(e)}")
            raise

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="question",
            output_key="answer"
        )

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

        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.knowledge_base.as_retriever(
                search_kwargs={"k": 4},
                search_type="similarity" 
            ),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": QA_PROMPT},
            return_source_documents=True,
            verbose=True,
            output_key="answer"  
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
            if not self._is_insurance_related(query):
                return (
                    "I'm an insurance specialist and can only answer questions related to insurance policies, "
                    "coverage, premiums, and claims. Could you please ask an insurance-related question?"
                )

            logger.info(f"Processing query: {query}")

            result = self.chain({"question": query})

            logger.info(f"Got result: {result.keys()}")
            
            answer = result['answer']
            source_docs = result.get('source_documents', [])
            
            if not source_docs or self._is_no_information_response(answer):
                return (
                    "I don't have enough information to answer that question completely. "
                    "Would you like me to connect you with a customer support executive who can provide you with more detailed information?"
                )

            if self._should_escalate(query, answer):
                return (
                    f"{answer}\n\n"
                    "For this specific query, it might be better to speak with one of our human insurance agents. "
                    "Would you like me to arrange for someone to contact you?"
                )

            return answer

        except Exception as e:
            logger.error(f"Error in get_response: {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())

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

    def _is_no_information_response(self, answer: str) -> bool:
        """
        Determine if the response indicates that no information was found.
        
        Args:
            answer: The generated answer
            
        Returns:
            Boolean indicating if the answer lacks information
        """
        no_info_indicators = [
            "I don't have enough information",
            "I don't have information", 
            "I cannot provide",
            "I don't have specific",
            "not included in",
            "not mentioned in",
            "not in the context",
            "not available in",
            "not specified in",
            "not found in",
            "I don't know",
            "I'm not sure",
            "cannot find",
            "no information about",
            "the provided context does not",
            "no details about",
            "cannot access",
            "do not have access",
            "not provided in"
        ]
        
        return any(indicator.lower() in answer.lower() for indicator in no_info_indicators)

    def _should_escalate(self, query: str, answer: str) -> bool:
        """
        Determine if a query should be escalated to a human agent.

        Args:
            query: The user query
            answer: The generated answer

        Returns:
            Boolean indicating if the query should be escalated
        """
        complex_indicators = [
            "would need more details",
            "cannot accurately",
            "specific to your situation",
            "recommend speaking with an agent",
            "cannot calculate",
            "varies depending on",
            "specific information",
            "not in my knowledge",
            "outside the scope",
            "detailed answer"
        ]

        complex_topics = [
            "lawsuit", "legal", "sue", "death", "dispute", "rejected claim",
            "denied", "appeal", "fraud", "investigation", "cancelation",
            "specific quote", "exact premium", "exact rate", "specific to my case",
            "personal information", "policy number", "payment information"
        ]

        query_lower = query.lower()
        return (
            any(indicator.lower() in answer.lower() for indicator in complex_indicators) or
            any(topic in query_lower for topic in complex_topics)
        )