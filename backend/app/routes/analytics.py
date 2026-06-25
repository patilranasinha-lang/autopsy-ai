from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.timeline_service import TimelineService
from app.services.statistics_service import StatisticsService
from app.services.insight_service import InsightService

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/timeline', methods=['GET'])
@jwt_required()
def get_timeline():
    try:
        current_user_id = int(get_jwt_identity())
        period = request.args.get('period', 'daily')
        
        timeline_data = TimelineService.get_timeline(current_user_id, period)
        
        return jsonify(timeline_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    try:
        current_user_id = int(get_jwt_identity())
        
        metrics = StatisticsService.get_behavioral_metrics(current_user_id)
        
        return jsonify(metrics), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/insights', methods=['GET'])
@jwt_required()
def get_insights():
    try:
        current_user_id = int(get_jwt_identity())
        
        insights = InsightService.generate_insights(current_user_id)
        
        return jsonify({"insights": insights}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/heatmap', methods=['GET'])
@jwt_required()
def get_heatmap():
    try:
        current_user_id = int(get_jwt_identity())
        
        heatmap_data = StatisticsService.get_heatmap_data(current_user_id)
        
        return jsonify(heatmap_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
