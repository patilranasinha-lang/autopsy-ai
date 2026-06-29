from datetime import datetime
import json

class IntelligenceSnapshot:
    def __init__(self, id, user_id, intelligence_summary, computed_at=None):
        self.id = id
        self.user_id = user_id
        self.intelligence_summary = intelligence_summary # dict/JSONB
        self.computed_at = computed_at or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'intelligence_summary': self.intelligence_summary,
            'computed_at': self.computed_at.isoformat() if hasattr(self.computed_at, 'isoformat') else self.computed_at
        }
