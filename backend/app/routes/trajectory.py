from flask import Blueprint, request, jsonify
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from analytics.trajectory.trajectory_scoring import TrajectoryScoring
from models.user_goal import UserGoal
from models.behavioral_trajectory import BehavioralTrajectory

trajectory_bp = Blueprint('trajectory', __name__, url_prefix='/trajectory')
scoring_engine = TrajectoryScoring()

MOCK_GOALS_DB = {}

@trajectory_bp.route('/goals', methods=['POST'])
def set_goal():
    data = request.json
    goal = UserGoal(
        id=len(MOCK_GOALS_DB) + 1,
        user_id=data.get('user_id'),
        goal_type=data.get('goal_type'),
        target_value=data.get('target_value'),
        time_frame=data.get('time_frame'),
        status='active'
    )
    MOCK_GOALS_DB[goal.id] = goal
    return jsonify(goal.to_dict()), 201

@trajectory_bp.route('/trends', methods=['GET'])
def get_trends():
    user_id = request.args.get('user_id')
    trend_data = scoring_engine.trend_detector.detect_macro_trend(user_id)
    return jsonify(trend_data)

@trajectory_bp.route('/forecast', methods=['GET'])
def get_forecast():
    user_id = request.args.get('user_id')
    goal_id = request.args.get('goal_id', type=int)
    
    current_activity = {
        "hours_completed": 12,
        "days_elapsed": 5,
        "total_days": 7,
        "current_streak": 5
    }
    
    goal_data = MOCK_GOALS_DB.get(goal_id, UserGoal(1, user_id, "Weekly Deep Work", 15.0, "week", "active")).to_dict()
    
    trajectory_data = scoring_engine.evaluate_trajectory(
        user_id=user_id,
        goal_data=goal_data,
        current_activity=current_activity
    )
    
    return jsonify({
        "goal": goal_data,
        "forecast": trajectory_data["goal_tracking"],
        "consistency": trajectory_data["consistency_forecast"]
    })

@trajectory_bp.route('/course-correct', methods=['GET'])
def get_course_correction():
    user_id = request.args.get('user_id')
    goal_id = request.args.get('goal_id', type=int)
    
    goal_data = MOCK_GOALS_DB.get(goal_id, UserGoal(1, user_id, "Weekly Deep Work", 15.0, "week", "active")).to_dict()
    
    current_activity = {
        "hours_completed": 12,
        "days_elapsed": 5,
        "total_days": 7,
        "current_streak": 5
    }
    
    trajectory_data = scoring_engine.evaluate_trajectory(
        user_id=user_id,
        goal_data=goal_data,
        current_activity=current_activity
    )
    
    return jsonify({
        "trajectory_status": trajectory_data["trajectory_status"],
        "course_correction": trajectory_data["course_correction"],
        "trend_detected": trajectory_data["trend_data"]["trend_type"]
    })
