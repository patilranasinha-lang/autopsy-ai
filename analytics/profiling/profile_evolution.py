from typing import List, Dict, Any
from datetime import datetime

class ProfileEvolution:
    """
    Tracks how the user's archetype changes over time.
    """
    
    def analyze_evolution(self, historical_profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Map out transitions between archetypes
        evolution = []
        for i in range(1, len(historical_profiles)):
            prev = historical_profiles[i-1]
            curr = historical_profiles[i]
            
            if prev["primary"] != curr["primary"]:
                evolution.append({
                    "date": curr.get("date", datetime.utcnow()),
                    "from_archetype": prev["primary"],
                    "to_archetype": curr["primary"]
                })
                
        return evolution
