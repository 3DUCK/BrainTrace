"""
Intent Analysis Service
-----------------------

This service analyzes the user's question to determine the intent.
It classifies the question into one of the following categories:
- SIMPLE: Simple greetings or general questions that do not require RAG or external agents.
- RAG: Questions that require searching the knowledge graph or documents.
- AGENT: Questions that require prediction, calculation, or analysis using external agents.
"""

import logging
import json
import re
from typing import Dict, Any
from services.base_ai_service import BaseAIService

class IntentService:
    def __init__(self, ai_service: BaseAIService):
        self.ai_service = ai_service

    def analyze_intent(self, question: str) -> Dict[str, Any]:
        """
        Analyzes the user's question and returns the intent and relevant parameters.

        Args:
            question (str): The user's question.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - intent: "SIMPLE", "RAG", or "AGENT"
                - params: (Optional) Extracted parameters for the agent
                - reason: The reason for the classification
        """
        prompt = (
            f"Analyze the following user question and classify it into one of three categories:\n"
            f"1. SIMPLE: Simple greetings, self-introductions, or general questions that don't need specific knowledge base search. (e.g., 'Hello', 'Who are you?')\n"
            f"2. RAG: Questions that require searching for specific information in documents or knowledge graphs. (e.g., 'What is the summary of document A?', 'Explain the concept of X.')\n"
            f"3. AGENT: Questions that require prediction, calculation, simulation, or analysis using specific data (e.g., pricing, ROI prediction, scenario analysis). (e.g., 'How should we set the price?', 'What if we reduce ad spend by 20%?')\n\n"
            f"User Question: {question}\n\n"
            f"Respond ONLY with a JSON object in the following format:\n"
            f"{{\n"
            f'  "intent": "SIMPLE" | "RAG" | "AGENT",\n'
            f'  "reason": "Brief explanation of why this category was chosen",\n'
            f'  "params": {{ "key": "value" }} // Extract relevant numbers or entities if intent is AGENT, otherwise empty dict\n'
            f"}}\n"
        )

        try:
            response = self.ai_service.chat(prompt)
            # Extract JSON from response if it contains other text
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                
                # Validate intent
                if result.get("intent") not in ["SIMPLE", "RAG", "AGENT"]:
                    logging.warning(f"Invalid intent detected: {result.get('intent')}. Defaulting to RAG.")
                    return {"intent": "RAG", "reason": "Invalid intent detected", "params": {}}
                
                return result
            else:
                logging.warning("Failed to parse JSON from IntentService response. Defaulting to RAG.")
                return {"intent": "RAG", "reason": "JSON parsing failed", "params": {}}

        except Exception as e:
            logging.error(f"Error in IntentService: {e}")
            return {"intent": "RAG", "reason": f"Error: {str(e)}", "params": {}}
