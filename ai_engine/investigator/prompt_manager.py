from typing import List, Dict, Any

class PromptManager:
    """
    Constructs strict system prompts forcing the LLM to act as a clinical, 
    data-driven behavioral scientist using ONLY the retrieved context.
    """
    
    def __init__(self):
        self.base_system_prompt = (
            "You are Autopsy AI, an elite, clinical, and data-driven behavioral scientist. "
            "Your goal is to analyze the user's habits and productivity data. "
            "You MUST base your conclusions strictly on the provided evidence context. "
            "If the context does not contain the answer, politely state that you do not have enough data. "
            "Do not invent facts or make assumptions outside the provided behavioral data."
        )
        
    def build_prompt(self, user_query: str, retrieved_context: List[Dict[str, Any]]) -> str:
        context_str = "\n".join([f"- {c['text']}" for c in retrieved_context])
        
        prompt = f"""
{self.base_system_prompt}

EVIDENCE CONTEXT:
{context_str}

USER QUERY:
{user_query}

Based ONLY on the evidence above, answer the user's query directly and clinically.
"""
        return prompt
