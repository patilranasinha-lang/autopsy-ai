from typing import List

class TrajectoryAnalyzer:
    """Analyzes trajectory modifiers based on current active habits."""
    
    def analyze(self, active_habits: List) -> float:
        modifier = 0.0
        
        for habit in active_habits:
            if habit.is_negative:
                # e.g., Late-night YouTube penalty
                modifier -= 5.0
            else:
                # e.g., Consistent morning deep work
                modifier += 3.0
                
        return modifier
