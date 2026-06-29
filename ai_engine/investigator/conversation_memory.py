from typing import List, Dict, Any

class ConversationMemory:
    """
    Manages short-term conversation context for the AI Investigator.
    """
    
    def __init__(self):
        # Mock in-memory store
        self.memory_store = {}
        
    def append_interaction(self, user_id: int, user_query: str, ai_response: str) -> None:
        if user_id not in self.memory_store:
            self.memory_store[user_id] = []
            
        self.memory_store[user_id].append({
            "query": user_query,
            "response": ai_response
        })
        
    def get_history(self, user_id: int) -> List[Dict[str, str]]:
        return self.memory_store.get(user_id, [])
