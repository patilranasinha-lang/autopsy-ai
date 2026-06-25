from app import db
from .core import TimestampMixin

class ProductivityScore(db.Model, TimestampMixin):
    __tablename__ = 'productivity_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    
    productivity_score = db.Column(db.Float, nullable=False, default=0.0)
    focus_score = db.Column(db.Float, nullable=False, default=0.0)
    consistency_score = db.Column(db.Float, nullable=False, default=0.0)
    discipline_score = db.Column(db.Float, nullable=False, default=0.0)
    deep_work_score = db.Column(db.Float, nullable=False, default=0.0)
    
    # Relationships
    user = db.relationship('User', back_populates='scores')
    
    # Ensure only one score per user per day
    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='uq_user_date_score'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'productivity_score': self.productivity_score,
            'focus_score': self.focus_score,
            'consistency_score': self.consistency_score,
            'discipline_score': self.discipline_score,
            'deep_work_score': self.deep_work_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
