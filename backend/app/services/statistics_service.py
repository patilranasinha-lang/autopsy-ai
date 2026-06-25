from typing import Dict, Any, List
from sqlalchemy import func
from app import db
from app.models.events import BehaviorEvent

class StatisticsService:
    @staticmethod
    def get_behavioral_metrics(user_id: int) -> Dict[str, Any]:
        """
        Calculates: Most active hour, least active hour, most active day, 
        average daily activity, and activity categories percentage.
        """
        # 1. Activity Categories Percentage
        category_counts = db.session.query(
            BehaviorEvent.category,
            func.count(BehaviorEvent.id).label('count')
        ).filter(
            BehaviorEvent.user_id == user_id,
            BehaviorEvent.category.isnot(None)
        ).group_by(BehaviorEvent.category).all()
        
        total_categorized = sum(row.count for row in category_counts)
        categories_percentage = {}
        if total_categorized > 0:
            for row in category_counts:
                categories_percentage[row.category] = round((row.count / total_categorized) * 100, 1)

        # 2. Hourly distribution
        if db.engine.name == 'sqlite':
            hour_expr = func.cast(func.strftime('%H', BehaviorEvent.timestamp), db.Integer)
        else:
            hour_expr = func.cast(func.extract('hour', BehaviorEvent.timestamp), db.Integer)
            
        hourly_counts = db.session.query(
            hour_expr.label('hour'),
            func.count(BehaviorEvent.id).label('count')
        ).filter(BehaviorEvent.user_id == user_id).group_by('hour').all()

        most_active_hour = None
        least_active_hour = None
        if hourly_counts:
            sorted_hours = sorted(hourly_counts, key=lambda x: x.count)
            least_active_hour_val = sorted_hours[0].hour
            most_active_hour_val = sorted_hours[-1].hour
            
            def format_hour(h):
                if h == 0: return "12AM"
                elif h < 12: return f"{h}AM"
                elif h == 12: return "12PM"
                else: return f"{h-12}PM"
                
            most_active_hour = format_hour(most_active_hour_val)
            least_active_hour = format_hour(least_active_hour_val)

        # 3. Daily distribution
        if db.engine.name == 'sqlite':
            day_expr = func.cast(func.strftime('%w', BehaviorEvent.timestamp), db.Integer) # 0-6, 0 is Sunday
        else:
            day_expr = func.cast(func.extract('dow', BehaviorEvent.timestamp), db.Integer) # 0-6, 0 is Sunday
            
        daily_counts = db.session.query(
            day_expr.label('dow'),
            func.count(BehaviorEvent.id).label('count')
        ).filter(BehaviorEvent.user_id == user_id).group_by('dow').all()

        most_active_day = None
        if daily_counts:
            sorted_days = sorted(daily_counts, key=lambda x: x.count, reverse=True)
            dow = sorted_days[0].dow
            days_map = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
            most_active_day = days_map.get(dow, "Unknown")
            
        # 4. Average daily activity
        if db.engine.name == 'sqlite':
            date_expr = func.date(BehaviorEvent.timestamp)
        else:
            date_expr = func.date_trunc('day', BehaviorEvent.timestamp)
            
        # days_active will return the number of distinct dates
        days_active = db.session.query(date_expr).filter(BehaviorEvent.user_id == user_id).distinct().count()
        total_events_query = db.session.query(func.count(BehaviorEvent.id)).filter(BehaviorEvent.user_id == user_id).scalar()
        total_events = total_events_query or 0
        
        avg_daily_activity = round(total_events / days_active, 1) if days_active > 0 else 0

        return {
            "most_active_hour": most_active_hour,
            "least_active_hour": least_active_hour,
            "most_active_day": most_active_day,
            "average_daily_activity": avg_daily_activity,
            "categories_percentage": categories_percentage
        }

    @staticmethod
    def get_heatmap_data(user_id: int) -> Dict[str, Any]:
        """
        Generate Day vs Hour heatmaps.
        """
        if db.engine.name == 'sqlite':
            day_expr = func.cast(func.strftime('%w', BehaviorEvent.timestamp), db.Integer)
            hour_expr = func.cast(func.strftime('%H', BehaviorEvent.timestamp), db.Integer)
        else:
            day_expr = func.cast(func.extract('dow', BehaviorEvent.timestamp), db.Integer)
            hour_expr = func.cast(func.extract('hour', BehaviorEvent.timestamp), db.Integer)

        results = db.session.query(
            day_expr.label('day'),
            hour_expr.label('hour'),
            func.count(BehaviorEvent.id).label('count')
        ).filter(
            BehaviorEvent.user_id == user_id
        ).group_by(
            'day', 'hour'
        ).all()
        
        matrix = [[0 for _ in range(24)] for _ in range(7)]
        
        for row in results:
            if row.day is not None and row.hour is not None:
                d = int(row.day)
                h = int(row.hour)
                if 0 <= d <= 6 and 0 <= h <= 23:
                    matrix[d][h] = row.count
                    
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        hours = [f"{h}:00" for h in range(24)]
        
        return {
            "x": hours,
            "y": days,
            "z": matrix
        }
