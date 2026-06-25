from typing import List, Dict, Any

class InsightEngine:
    @staticmethod
    def generate_insights(current_scores: Dict[str, float], previous_scores: Dict[str, float] = None) -> List[str]:
        insights = []
        
        # Basic daily insights
        deep_work_hours = round(current_scores.get('deep_work_score', 0) * 1.8 / 100, 1) # ~3h max translated
        if deep_work_hours > 0:
            insights.append(f"You achieved {deep_work_hours} hours of equivalent deep work today.")
            
        if current_scores.get('focus_score', 0) < 50:
            insights.append("Context switching heavily reduced your focus score today.")
            
        # Comparison insights
        if previous_scores:
            prod_delta = current_scores.get('productivity_score', 0) - previous_scores.get('productivity_score', 0)
            if prod_delta > 5:
                insights.append(f"Your productivity score increased {round(prod_delta)} points compared to yesterday.")
            elif prod_delta < -5:
                insights.append(f"Your productivity score dropped {round(abs(prod_delta))} points compared to yesterday.")
                
            disc_delta = current_scores.get('discipline_score', 0) - previous_scores.get('discipline_score', 0)
            if disc_delta < -10:
                insights.append("You spent significantly more time on entertainment/distractions compared to yesterday.")
                
        if not insights:
            insights.append("Consistency is key. Keep maintaining your routine!")
            
        return insights
