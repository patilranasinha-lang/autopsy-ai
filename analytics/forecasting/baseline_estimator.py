from typing import List

class BaselineEstimator:
    """Estimates the long-term baseline productivity score using EMA."""
    
    def estimate(self, historical_scores: List) -> float:
        if not historical_scores:
            return 50.0 # Default starting baseline
            
        # Extract the last 30 days of scores
        scores = [s.score for s in historical_scores[-30:]]
        
        # Simple Exponential Moving Average (EMA)
        alpha = 0.2
        ema = scores[0]
        for score in scores[1:]:
            ema = (score * alpha) + (ema * (1 - alpha))
            
        return ema
