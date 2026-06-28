from datetime import datetime

class BehavioralTrajectory:
    def __init__(self, id, user_id, macro_trend_type, goal_id, target_metric, current_trajectory_status, consistency_probability, created_at=None):
        self.id = id
        self.user_id = user_id
        self.macro_trend_type = macro_trend_type
        self.goal_id = goal_id
        self.target_metric = target_metric
        self.current_trajectory_status = current_trajectory_status
        self.consistency_probability = consistency_probability
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'macro_trend_type': self.macro_trend_type,
            'goal_id': self.goal_id,
            'target_metric': self.target_metric,
            'current_trajectory_status': self.current_trajectory_status,
            'consistency_probability': self.consistency_probability,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at
        }
