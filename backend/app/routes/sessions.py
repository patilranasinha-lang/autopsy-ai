from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.session_service import SessionService

sessions_bp = Blueprint('sessions', __name__)

@sessions_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_sessions():
    try:
        current_user_id = int(get_jwt_identity())
        count = SessionService.generate_sessions_for_user(current_user_id)
        return jsonify({"message": f"Successfully generated {count} sessions", "count": count}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('', methods=['GET'])
@jwt_required()
def get_sessions():
    try:
        current_user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        data = SessionService.get_sessions(current_user_id, page, per_page)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('/<int:session_id>', methods=['GET'])
@jwt_required()
def get_session(session_id):
    try:
        current_user_id = int(get_jwt_identity())
        session = SessionService.get_session_by_id(current_user_id, session_id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        return jsonify(session), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    try:
        current_user_id = int(get_jwt_identity())
        summary = SessionService.get_session_summary(current_user_id)
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
