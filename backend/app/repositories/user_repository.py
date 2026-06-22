from app.repositories.base_repository import BaseRepository
from app.models import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
        
    def get_by_username(self, username: str):
        return User.query.filter_by(username=username).first()
        
    def get_by_email(self, email: str):
        return User.query.filter_by(email=email).first()
