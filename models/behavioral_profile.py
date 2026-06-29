from datetime import datetime
import uuid

class BehavioralProfile:
    def __init__(self, id, user_id, primary_archetype, secondary_archetype, segment_cluster_id=None, computed_at=None):
        self.id = id
        self.user_id = user_id
        self.primary_archetype = primary_archetype
        self.secondary_archetype = secondary_archetype
        self.segment_cluster_id = segment_cluster_id or str(uuid.uuid4())
        self.computed_at = computed_at or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'primary_archetype': self.primary_archetype,
            'secondary_archetype': self.secondary_archetype,
            'segment_cluster_id': str(self.segment_cluster_id),
            'computed_at': self.computed_at.isoformat() if hasattr(self.computed_at, 'isoformat') else self.computed_at
        }
