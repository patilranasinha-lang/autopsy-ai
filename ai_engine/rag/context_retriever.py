from typing import List, Dict, Any
from .local_embedder import LocalEmbedder
from .vector_store import VectorStore

class ContextRetriever:
    """
    Orchestrates the retrieval pipeline. Embeds the user query, performs a vector 
    similarity search, and pulls the top-k most relevant behavioral facts.
    """
    
    def __init__(self):
        self.embedder = LocalEmbedder()
        self.vector_store = VectorStore()
        
    def retrieve_context(self, user_id: int, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.embed_text(query)
        relevant_chunks = self.vector_store.search_similarity(user_id, query_embedding, top_k)
        
        # Optionally, format the chunks for the LLM
        return relevant_chunks
