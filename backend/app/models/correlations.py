from app import db
from datetime import datetime

class BehaviorCorrelation(db.Model):
    __tablename__ = 'behavior_correlations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # e.g., "Music Before Study", "Coding Session Length"
    factor = db.Column(db.String(255), nullable=False)
    
    # e.g., "Productivity Score", "Focus Score", "Consistency Score"
    outcome = db.Column(db.String(255), nullable=False)
    
    # -1.0 to 1.0 (Pearson/Spearman coefficient)
    correlation_strength = db.Column(db.Float, nullable=False)
    
    # 0 to 100 based on p-value equivalent or sample size
    confidence_score = db.Column(db.Float, nullable=False)
    
    # Positive, Negative, Weak, Emerging
    relationship_type = db.Column(db.String(50), nullable=False)
    
    # Explanation
    explanation = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'factor': self.factor,
            'outcome': self.outcome,
            'correlation_strength': self.correlation_strength,
            'confidence_score': self.confidence_score,
            'relationship_type': self.relationship_type,
            'explanation': self.explanation,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
