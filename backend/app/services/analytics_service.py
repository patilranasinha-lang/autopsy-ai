from typing import Dict, Any
from sqlalchemy import func
from app import db
from app.models.events import BehaviorEvent

class AnalyticsService:
    @staticmethod
    def get_category_distribution(user_id: int) -> Dict[str, Any]:
        """
        Get the count of events grouped by category for a specific user.
        Useful for rendering pie charts or donut charts.
        """
        results = db.session.query(
            BehaviorEvent.category,
            func.count(BehaviorEvent.id).label('count')
        ).filter(
            BehaviorEvent.user_id == user_id
        ).group_by(
            BehaviorEvent.category
        ).all()

        distribution = {row.category: row.count for row in results}
        
        return {
            "total_events": sum(distribution.values()),
            "distribution": distribution
        }
