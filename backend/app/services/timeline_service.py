from typing import Dict, Any, List
from sqlalchemy import func
from app import db
from app.models.events import BehaviorEvent

class TimelineService:
    @staticmethod
    def get_timeline(user_id: int, period: str = 'daily') -> Dict[str, Any]:
        """
        Get activity timeline grouped by period ('daily', 'weekly', 'monthly').
        """
        if db.engine.name == 'sqlite':
            if period == 'monthly':
                time_column = func.strftime('%Y-%m', BehaviorEvent.timestamp)
            elif period == 'weekly':
                # %Y-%W yields Year and Week Number
                time_column = func.strftime('%Y-%W', BehaviorEvent.timestamp)
            else:
                time_column = func.date(BehaviorEvent.timestamp)
        else:
            if period == 'monthly':
                time_column = func.date_trunc('month', BehaviorEvent.timestamp)
            elif period == 'weekly':
                time_column = func.date_trunc('week', BehaviorEvent.timestamp)
            else:
                time_column = func.date_trunc('day', BehaviorEvent.timestamp)

        results = db.session.query(
            time_column.label('time_period'),
            func.count(BehaviorEvent.id).label('count')
        ).filter(
            BehaviorEvent.user_id == user_id
        ).group_by(
            time_column
        ).order_by(
            time_column
        ).all()

        timeline = []
        for row in results:
            if row.time_period:
                if isinstance(row.time_period, str):
                    date_str = row.time_period.split(' ')[0]
                else:
                    # Depending on PostgreSQL returning date or datetime
                    date_str = row.time_period.strftime('%Y-%m-%d')
                timeline.append({
                    "date": date_str,
                    "count": row.count
                })

        return {"period": period, "timeline": timeline}
