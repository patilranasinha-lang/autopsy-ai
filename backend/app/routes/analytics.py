from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    try:
        current_user_id = int(get_jwt_identity())
        
        category_data = AnalyticsService.get_category_distribution(current_user_id)
        time_series_data = AnalyticsService.get_activity_over_time(current_user_id)
        
        return jsonify({
            "category_distribution": category_data,
            "activity_over_time": time_series_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
