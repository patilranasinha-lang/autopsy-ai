from typing import List, Dict, Any

class ArchetypeClassifier:
    """
    Categorizes the user into dynamic behavioral archetypes based on 30-day baseline data.
    Designed to run as a background task.
    """
    
    def classify(self, historical_data: List[Any]) -> Dict[str, str]:
        if not historical_data:
            return {"primary": "Unknown", "secondary": "Unknown"}
            
        # Mock logic representing heuristic decision trees or K-Means cluster matching
        late_night_sessions = sum(1 for d in historical_data if getattr(d, 'is_late_night', False))
        deep_work_ratio = sum(getattr(d, 'deep_work_minutes', 0) for d in historical_data) / (len(historical_data) * 60) if historical_data else 0
        
        primary = "Standard Worker"
        secondary = "Balanced"
        
        if deep_work_ratio > 3.0:
            primary = "Deep Worker"
        
        if late_night_sessions > len(historical_data) * 0.4:
            secondary = "Night Owl"
        elif late_night_sessions == 0:
            secondary = "Early Bird"
            
        return {
            "primary": primary,
            "secondary": secondary
        }
