import logging
from typing import Optional
from app.repositories import UserRepository
from app.models import User

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
        
    def create_user(self, username: str, email: str, password: str) -> Optional[User]:
        if not username or not email or not password:
            raise ValueError('Username, email, and password are required')
            
        if self.user_repo.get_by_username(username):
            raise ValueError('Username already exists')
            
        if self.user_repo.get_by_email(email):
            raise ValueError('Email already exists')
            
        user = User(username=username, email=email)
        user.set_password(password)
        self.user_repo.create(user)
        
        logger.info(f'User created: {username}')
        return user
        
    def get_all_users(self, page: int = 1, per_page: int = 20):
        return self.user_repo.get_all(page, per_page)
        
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repo.get_by_id(user_id)
