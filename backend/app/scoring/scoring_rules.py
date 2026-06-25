from abc import ABC, abstractmethod
from typing import List
from app.models.sessions import BehaviorSession

def normalize_score(score: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """
    Ensures a calculated score strictly falls within the bounds [0.0, 100.0]
    """
    return round(max(min_val, min(max_val, score)), 2)

class BaseScoringEngine(ABC):
    @abstractmethod
    def calculate(self, daily_sessions: List[BehaviorSession], historical_sessions: List[BehaviorSession] = None) -> float:
        """
        Calculates a specific score (0-100) based on sessions.
        `historical_sessions` is used by engines that need trend context (e.g. ConsistencyEngine)
        """
        pass
