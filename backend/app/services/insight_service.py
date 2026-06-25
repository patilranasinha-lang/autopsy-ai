from typing import List, Dict, Any
from app.services.statistics_service import StatisticsService

class InsightService:
    @staticmethod
    def generate_insights(user_id: int) -> List[Dict[str, str]]:
        """
        Generate simple rule-based insights for V1 engine.
        """
        metrics = StatisticsService.get_behavioral_metrics(user_id)
        insights = []

        # 1. Most active hour insight
        most_active_hour = metrics.get('most_active_hour')
        if most_active_hour:
            insights.append({
                "type": "productivity",
                "text": f"Your highest activity occurs around {most_active_hour}."
            })
            
        # 2. Most active day
        most_active_day = metrics.get('most_active_day')
        if most_active_day:
            insights.append({
                "type": "routine",
                "text": f"{most_active_day} is typically your most active day of the week."
            })

        # 3. Category comparison
        categories = metrics.get('categories_percentage', {})
        if categories:
            sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
            if len(sorted_cats) >= 2:
                top_cat = sorted_cats[0][0]
                second_cat = sorted_cats[1][0]
                insights.append({
                    "type": "behavior",
                    "text": f"You spend more time on {top_cat} ({sorted_cats[0][1]}%) than {second_cat} ({sorted_cats[1][1]}%)."
                })
            elif len(sorted_cats) == 1:
                top_cat = sorted_cats[0][0]
                insights.append({
                    "type": "behavior",
                    "text": f"Your primary activity is {top_cat}, taking up {sorted_cats[0][1]}% of your time."
                })

        # 4. A generic average activity insight
        avg_activity = metrics.get('average_daily_activity')
        if avg_activity and avg_activity > 0:
            insights.append({
                "type": "summary",
                "text": f"You generate an average of {avg_activity} events per active day."
            })
            
        # Default fallback
        if not insights:
            insights.append({
                "type": "info",
                "text": "Upload more data to unlock deeper behavioral insights."
            })

        return insights
