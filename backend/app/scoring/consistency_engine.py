from typing import List
from datetime import datetime
from app.models.sessions import BehaviorSession
from .scoring_rules import BaseScoringEngine, normalize_score

class ConsistencyEngine(BaseScoringEngine):
    def calculate(self, daily_sessions: List[BehaviorSession], historical_sessions: List[BehaviorSession] = None) -> float:
        if not daily_sessions:
            return 0.0
            
        base_score = 50.0
        
        # If we have history, check streaks and variance
        if historical_sessions:
            # Group by date
            active_days = set([s.start_time.date() for s in historical_sessions])
            
            # Simple streak bonus
            streak_bonus = min(30.0, len(active_days) * 5.0)
            
            # Consistent start time bonus (routine)
            start_hours = [s.start_time.hour for s in historical_sessions]
            if start_hours:
                avg_start = sum(start_hours) / len(start_hours)
                variance = sum((h - avg_start) ** 2 for h in start_hours) / len(start_hours)
                
                # Lower variance -> higher routine -> more consistency
                routine_bonus = max(0.0, 20.0 - variance)
            else:
                routine_bonus = 0.0
                
            base_score += streak_bonus + routine_bonus
        else:
            # First day bonus
            base_score += 25.0
            
        return normalize_score(base_score)
