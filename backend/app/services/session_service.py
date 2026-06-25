from typing import Dict, Any, List
from sqlalchemy import func
from app import db
from app.models.events import BehaviorEvent
from app.models.sessions import BehaviorSession
from app.session_detection import SessionDetector, SESSION_TYPES

class SessionService:
    @staticmethod
    def generate_sessions_for_user(user_id: int) -> int:
        """
        Generates sessions from all events of a user.
        Deletes existing sessions first to avoid duplicates.
        Returns the number of sessions generated.
        """
        # Clean up old sessions
        db.session.query(BehaviorSession).filter_by(user_id=user_id).delete()
        db.session.commit()

        # Fetch events chronologically
        events = db.session.query(BehaviorEvent).filter_by(user_id=user_id).order_by(BehaviorEvent.timestamp).all()
        
        detector = SessionDetector(gap_threshold_minutes=15)
        sessions = detector.detect_sessions(events)
        
        if sessions:
            db.session.add_all(sessions)
            db.session.commit()
            
        return len(sessions)

    @staticmethod
    def get_sessions(user_id: int, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Retrieve paginated sessions for a user.
        """
        query = db.session.query(BehaviorSession).filter_by(user_id=user_id).order_by(BehaviorSession.start_time.desc())
        paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            "total": paginated.total,
            "pages": paginated.pages,
            "current_page": page,
            "sessions": [s.to_dict() for s in paginated.items]
        }

    @staticmethod
    def get_session_by_id(user_id: int, session_id: int) -> Dict[str, Any]:
        session = db.session.query(BehaviorSession).filter_by(user_id=user_id, id=session_id).first()
        if not session:
            return None
        return session.to_dict()

    @staticmethod
    def get_session_summary(user_id: int) -> Dict[str, Any]:
        """
        Generates:
        - Total sessions
        - Longest session
        - Average session duration
        - Deep work hours
        - Entertainment hours
        - Context switching frequency
        """
        sessions = db.session.query(BehaviorSession).filter_by(user_id=user_id).all()
        total_sessions = len(sessions)
        
        if total_sessions == 0:
            return {
                "total_sessions": 0,
                "longest_session_minutes": 0,
                "average_duration_minutes": 0,
                "deep_work_hours": 0,
                "entertainment_hours": 0,
                "context_switching_score": 0,
                "session_distribution": {}
            }
            
        longest = max(s.duration_minutes for s in sessions)
        avg_duration = sum(s.duration_minutes for s in sessions) / total_sessions
        
        deep_work_minutes = sum(s.duration_minutes for s in sessions if s.session_type == SESSION_TYPES["DEEP_WORK"])
        entertainment_minutes = sum(s.duration_minutes for s in sessions if s.session_type == SESSION_TYPES["ENTERTAINMENT"])
        
        context_switches = sum(1 for s in sessions if s.session_type == SESSION_TYPES["CONTEXT_SWITCHING"])
        context_switching_score = round((context_switches / total_sessions) * 100, 1)
        
        distribution = {}
        for s in sessions:
            distribution[s.session_type] = distribution.get(s.session_type, 0) + 1

        return {
            "total_sessions": total_sessions,
            "longest_session_minutes": round(longest, 1),
            "average_duration_minutes": round(avg_duration, 1),
            "deep_work_hours": round(deep_work_minutes / 60, 2),
            "entertainment_hours": round(entertainment_minutes / 60, 2),
            "context_switching_score": context_switching_score,
            "session_distribution": distribution
        }
