import logging
from flask import Blueprint, request, jsonify
from app.services import UserService

logger = logging.getLogger(__name__)

users_bp = Blueprint('users', __name__)
user_service = UserService()


@users_bp.route('', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        user = user_service.create_user(username, email, password)
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        logger.error(f'User creation error: {str(e)}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Unexpected error creating user: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


@users_bp.route('', methods=['GET'])
def get_users():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        result = user_service.get_all_users(page, per_page)
        return jsonify({
            'items': [user.to_dict() for user in result['items']],
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'pages': result['pages']
        }), 200
    except Exception as e:
        logger.error(f'Error fetching users: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = user_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict()), 200
    except Exception as e:
        logger.error(f'Error fetching user {user_id}: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500
