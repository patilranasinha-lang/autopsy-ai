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

    @staticmethod
    def get_activity_over_time(user_id: int) -> Dict[str, Any]:
        """
        Get the count of events grouped by day for a specific user.
        Useful for rendering line charts or bar charts over time.
        """
        # Truncate timestamp to day for PostgreSQL
        day_column = func.date_trunc('day', BehaviorEvent.timestamp)
        
        results = db.session.query(
            day_column.label('date'),
            func.count(BehaviorEvent.id).label('count')
        ).filter(
            BehaviorEvent.user_id == user_id
        ).group_by(
            day_column
        ).order_by(
            day_column
        ).all()

        timeline = []
        for row in results:
            if row.date:
                # Format datetime object to string YYYY-MM-DD
                date_str = row.date.strftime('%Y-%m-%d')
                timeline.append({
                    "date": date_str,
                    "count": row.count
                })

        return {"timeline": timeline}
