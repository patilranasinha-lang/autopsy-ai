from datetime import datetime

class UserGoal:
    def __init__(self, id, user_id, goal_type, target_value, time_frame, status, created_at=None):
        self.id = id
        self.user_id = user_id
        self.goal_type = goal_type # e.g., 'Weekly Deep Work'
        self.target_value = target_value # e.g., 15.0
        self.time_frame = time_frame # e.g., 'week'
        self.status = status # 'active', 'completed', 'abandoned'
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'goal_type': self.goal_type,
            'target_value': self.target_value,
            'time_frame': self.time_frame,
            'status': self.status,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at
        }
