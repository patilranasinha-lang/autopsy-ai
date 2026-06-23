import re
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class AuthValidator:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format using RFC-compliant regex"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
    
    @staticmethod
    def is_valid_password(password: str) -> bool:
        """Validate password strength: min 8 characters"""
        return len(password) >= 8
    
    @staticmethod
    def validate_registration(data: Dict) -> Tuple[bool, Optional[str]]:
        """Validate registration input"""
        required_fields = ['username', 'email', 'password']
        
        for field in required_fields:
            if field not in data or not data[field]:
                logger.warning(f"Registration validation failed: missing {field}")
                return False, f"{field} is required"
        
        username = data['username'].strip()
        email = data['email'].strip()
        password = data['password']
        
        if len(username) < 3:
            logger.warning("Registration validation failed: username too short")
            return False, "Username must be at least 3 characters"
        
        if not AuthValidator.is_valid_email(email):
            logger.warning(f"Registration validation failed: invalid email format")
            return False, "Invalid email format"
        
        if not AuthValidator.is_valid_password(password):
            logger.warning("Registration validation failed: password too short")
            return False, "Password must be at least 8 characters"
        
        return True, None
    
    @staticmethod
    def validate_login(data: Dict) -> Tuple[bool, Optional[str]]:
        """Validate login input"""
        required_fields = ['email', 'password']
        
        for field in required_fields:
            if field not in data or not data[field]:
                logger.warning(f"Login validation failed: missing {field}")
                return False, f"{field} is required"
        
        return True, None
