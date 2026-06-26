from datetime import datetime
from app import db


class Habit(db.Model):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    habit_name = db.Column(db.String(128), nullable=False)
    habit_type = db.Column(db.String(64), nullable=False) # e.g., 'Study', 'Coding', 'Productivity'
    
    confidence_score = db.Column(db.Float, nullable=False, default=0.0) # 0-100
    frequency = db.Column(db.Integer, nullable=False, default=1)
    
    first_detected = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_detected = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    description = db.Column(db.Text, nullable=True) # E.g., "User begins coding between 9 PM and 10 PM on 82% of active days."
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='habits')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'habit_name': self.habit_name,
            'habit_type': self.habit_type,
            'confidence_score': self.confidence_score,
            'frequency': self.frequency,
            'first_detected': self.first_detected.isoformat() if self.first_detected else None,
            'last_detected': self.last_detected.isoformat() if self.last_detected else None,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Habit {self.habit_name} (Score: {self.confidence_score})>"
