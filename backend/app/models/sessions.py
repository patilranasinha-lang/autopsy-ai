from app import db
from .core import TimestampMixin

class BehaviorSession(db.Model, TimestampMixin):
    __tablename__ = 'behavior_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('uploads.id', ondelete='CASCADE'), nullable=True, index=True)
    
    session_type = db.Column(db.String(100), nullable=False, index=True)
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, nullable=False, index=True)
    duration_minutes = db.Column(db.Float, nullable=False)
    event_count = db.Column(db.Integer, nullable=False, default=0)
    productivity_score = db.Column(db.Float, nullable=True)
    
    # Relationships
    user = db.relationship('User', back_populates='sessions')
    upload = db.relationship('Upload', back_populates='sessions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'upload_id': self.upload_id,
            'session_type': self.session_type,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_minutes': self.duration_minutes,
            'event_count': self.event_count,
            'productivity_score': self.productivity_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
