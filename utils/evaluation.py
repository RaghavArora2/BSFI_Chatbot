"""
Evaluation utilities for the insurance policy chatbot.
This module provides functions to evaluate response quality and collect user feedback.
"""

import streamlit as st
from typing import Dict, Any, List, Tuple
import re

def extract_policy_entities(text: str) -> List[str]:
    """
    Extract insurance policy entity mentions from text.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        List[str]: List of policy entities found
    """
    # Common insurance policy types and terms
    policy_terms = [
        "auto insurance", "car insurance", "vehicle insurance",
        "health insurance", "medical insurance", "healthcare plan",
        "home insurance", "homeowners insurance", "property insurance",
        "life insurance", "term life", "whole life", "universal life",
        "liability coverage", "collision coverage", "comprehensive coverage",
        "deductible", "premium", "claim", "policyholder", "beneficiary",
        "coverage limit", "exclusion", "rider", "underwriting"
    ]
    
    found_terms = []
    for term in policy_terms:
        if re.search(r'\b' + re.escape(term) + r'\b', text.lower()):
            found_terms.append(term)
    
    return found_terms

def assess_response_quality(query: str, response: str) -> Dict[str, Any]:
    """
    Perform basic assessment of response quality.
    
    Args:
        query (str): The user's query
        response (str): The system's response
        
    Returns:
        Dict[str, Any]: Quality assessment metrics
    """
    # Extract policy terms mentioned
    policy_terms = extract_policy_entities(response)
    
    # Calculate basic metrics
    word_count = len(response.split())
    sentence_count = len(re.split(r'[.!?]+', response))
    contains_markdown = bool(re.search(r'[*#_`]', response))
    contains_uncertain_phrases = bool(re.search(
        r'\b(might|may|possibly|probably|uncertain|unclear|don\'t have enough|can\'t determine)\b', 
        response.lower()
    ))
    
    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "policy_terms_count": len(policy_terms),
        "policy_terms": policy_terms,
        "contains_markdown": contains_markdown,
        "contains_uncertain_phrases": contains_uncertain_phrases,
        "estimated_response_quality": "high" if word_count > 50 and len(policy_terms) > 1 and not contains_uncertain_phrases else "medium"
    }

def collect_user_feedback(query_id: str) -> Tuple[bool, bool, str]:
    """
    Collect user feedback on response quality.
    
    Args:
        query_id (str): Identifier for the query-response pair
        
    Returns:
        Tuple[bool, bool, str]: (helpful, clear, feedback_text)
    """
    st.write("##### Was this response helpful?")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        helpful = st.button("👍 Yes", key=f"helpful_{query_id}")
    
    with col2:
        not_helpful = st.button("👎 No", key=f"not_helpful_{query_id}")
    
    with col3:
        feedback_text = st.text_input("Additional feedback (optional)", key=f"feedback_{query_id}")
    
    return helpful, not_helpful, feedback_text

def store_feedback(query_id: str, is_helpful: bool, feedback_text: str = "") -> None:
    """
    Store user feedback in session state.
    
    Args:
        query_id (str): Identifier for the query-response pair
        is_helpful (bool): Whether the user found the response helpful
        feedback_text (str): Additional feedback text
    """
    st.session_state.feedback_collected[query_id] = {
        "helpful": is_helpful,
        "feedback_text": feedback_text,
        "timestamp": st.session_state.get("_current_time", None)
    }

def analyze_query_difficulty(query: str) -> str:
    """
    Analyze the difficulty level of a user query.
    
    Args:
        query (str): The user's query
        
    Returns:
        str: Difficulty level ('basic', 'intermediate', 'complex')
    """
    # Count words to estimate complexity
    word_count = len(query.split())
    
    # Check for specific question patterns
    has_comparison = bool(re.search(r'\b(compare|difference|versus|vs\.?|better)\b', query.lower()))
    has_specific_details = bool(re.search(r'\b(specific|exactly|detail|precise)\b', query.lower()))
    has_multiple_questions = len(re.split(r'[?]+', query)) > 2
    has_hypothetical = bool(re.search(r'\b(what if|suppose|scenario|hypothetical)\b', query.lower()))
    
    # Count policy terms
    policy_terms = extract_policy_entities(query)
    
    # Determine difficulty level
    if len(policy_terms) >= 2 or has_comparison or has_hypothetical or has_multiple_questions:
        return "complex"
    elif has_specific_details or word_count > 15 or len(policy_terms) == 1:
        return "intermediate"
    else:
        return "basic"
