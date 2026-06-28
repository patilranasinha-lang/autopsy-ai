from datetime import datetime
import json

class ProductivityForecast:
    def __init__(self, id, user_id, target_date, forecasted_productivity_score, forecasted_deep_work_minutes, trajectory_trend, confidence_interval, momentum_factors, created_at=None):
        self.id = id
        self.user_id = user_id
        self.target_date = target_date
        self.forecasted_productivity_score = forecasted_productivity_score
        self.forecasted_deep_work_minutes = forecasted_deep_work_minutes
        self.trajectory_trend = trajectory_trend
        self.confidence_interval = confidence_interval
        self.momentum_factors = momentum_factors
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        try:
            factors = json.loads(self.momentum_factors) if isinstance(self.momentum_factors, str) else self.momentum_factors
        except:
            factors = {}
            
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_date': self.target_date.isoformat() if hasattr(self.target_date, 'isoformat') else self.target_date,
            'forecasted_productivity_score': self.forecasted_productivity_score,
            'forecasted_deep_work_minutes': self.forecasted_deep_work_minutes,
            'trajectory_trend': self.trajectory_trend,
            'confidence_interval': self.confidence_interval,
            'momentum_factors': factors,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at
        }
