from typing import List, Dict, Any

class ConfidenceScorer:
    """Calculates confidence of predictions based on routine consistency."""
    
    def score(self, window: Dict[str, Any], sessions: List) -> float:
        # Base confidence
        confidence = 70.0
        
        # If user has lots of data, increase confidence
        if len(sessions) > 50:
            confidence += 15.0
            
        # Hard cap at 95%
        return min(95.0, confidence)
