from typing import List, Dict, Any
from .prompt_manager import PromptManager
from ai_engine.rag.context_retriever import ContextRetriever

class LLMOrchestrator:
    """
    Orchestrates the entire AI Investigator interaction.
    1. Retrieves Context
    2. Builds Prompt
    3. Calls LLM (Mocked here)
    """
    
    def __init__(self):
        self.retriever = ContextRetriever()
        self.prompt_manager = PromptManager()
        
    def process_query(self, user_id: int, query: str) -> Dict[str, Any]:
        # 1. Retrieve relevant facts
        context = self.retriever.retrieve_context(user_id, query)
        
        # 2. Build strict prompt
        prompt = self.prompt_manager.build_prompt(query, context)
        
        # 3. Call LLM (Mocked)
        # Assuming the context tells us about context-switching and YouTube
        response_text = "According to your behavioral snapshot, your context-switching increased by 40% over the last 3 days, primarily driven by late-night YouTube sessions, which is fracturing your deep work."
        
        return {
            "response": response_text,
            "evidence_used": context
        }
