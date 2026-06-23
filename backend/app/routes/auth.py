from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from app.services import AuthService
from app.validators import AuthValidator

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)
auth_service = AuthService()


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    POST /api/auth/register
    """
    data = request.get_json() or {}
    
    # Validate input
    is_valid, error_msg = AuthValidator.validate_registration(data)
    if not is_valid:
        return jsonify({
            'success': False,
            'message': error_msg
        }), 400
    
    # Register user
    user, error = auth_service.register_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    if error:
        return jsonify({
            'success': False,
            'message': error
        }), 400
    
    # Return sanitized user data (no password)
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'data': {
            'user': user.to_dict()
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login a user
    POST /api/auth/login
    """
    data = request.get_json() or {}
    
    # Validate input
    is_valid, error_msg = AuthValidator.validate_login(data)
    if not is_valid:
        # Generic error to prevent enumeration
        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401
    
    # Login user
    access_token, error = auth_service.login_user(
        email=data['email'],
        password=data['password']
    )
    
    if error:
        # Generic error to prevent enumeration
        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'data': {
            'access_token': access_token
        }
    }), 200


@auth_bp.route('/profile/<int:user_id>', methods=['GET'])
@jwt_required()
def get_profile(user_id):
    """
    Get user profile (requires authentication)
    GET /api/auth/profile/<user_id>
    """
    current_user_id = get_jwt_identity()
    
    # Get user profile
    user = auth_service.get_user_profile(user_id)
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': {
            'user': user.to_dict()
        }
    }), 200

