from flask import Blueprint, jsonify, request
from analytics.graph.behavioral_graph import BehavioralGraph
from analytics.graph.anomaly_detector import AnomalyDetector

digital_twin_bp = Blueprint('digital_twin', __name__, url_prefix='/api/digital-twin')

@digital_twin_bp.route('/state', methods=['GET'])
def get_digital_twin_state():
    user_id = request.args.get('user_id')
    
    # Mock data retrieval for user's habits and correlations
    mock_habits = [
        {"id": "h1", "name": "Late Night Coding"},
        {"id": "h2", "name": "Morning Exercise"},
        {"id": "h3", "name": "Deep Work Block"}
    ]
    mock_correlations = [
        {"source_id": "h1", "target_id": "h3", "correlation_strength": -0.8},
        {"source_id": "h2", "target_id": "h3", "correlation_strength": 0.6}
    ]
    
    # 1. Graph Engine
    graph_engine = BehavioralGraph()
    graph_engine.build_graph(user_id, mock_habits, mock_correlations)
    central_habits = graph_engine.detect_central_habits()
    
    # 2. Anomaly Detection
    anomaly_detector = AnomalyDetector(threshold=2.0)
    mock_recent_scores = [80, 85, 82, 40, 81, 79, 88] # 40 is an anomaly
    anomalies = anomaly_detector.detect_anomalies(mock_recent_scores)
    
    response = {
        "user_id": user_id,
        "ecosystem_graph": graph_engine.get_graph_data(),
        "central_influencers": central_habits,
        "recent_anomalies": anomalies
    }
    
    return jsonify(response)
