from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.habit_service import HabitService
from app.models.habits import Habit

habits_bp = Blueprint('habits', __name__)

@habits_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_habits():
    current_user_id = int(get_jwt_identity())
    try:
        habits = HabitService.generate_habits_for_user(current_user_id)
        return jsonify({
            "message": "Habits detected successfully",
            "count": len(habits),
            "habits": [h.to_dict() for h in habits]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@habits_bp.route('', methods=['GET'])
@jwt_required()
def get_habits():
    current_user_id = int(get_jwt_identity())
    habits = HabitService.get_habits(current_user_id)
    return jsonify({"habits": [h.to_dict() for h in habits]}), 200

@habits_bp.route('/<int:habit_id>', methods=['GET'])
@jwt_required()
def get_habit(habit_id):
    current_user_id = int(get_jwt_identity())
    habit = Habit.query.filter_by(id=habit_id, user_id=current_user_id).first()
    if not habit:
        return jsonify({"error": "Habit not found"}), 404
    return jsonify(habit.to_dict()), 200

@habits_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_habit_summary():
    current_user_id = int(get_jwt_identity())
    summary = HabitService.get_habit_summary(current_user_id)
    return jsonify(summary), 200
    
@habits_bp.route('/triggers', methods=['GET'])
@jwt_required()
def get_triggers():
    """Specific endpoint to fetch just trigger-based habits."""
    current_user_id = int(get_jwt_identity())
    habits = Habit.query.filter_by(user_id=current_user_id).filter(
        Habit.habit_name.like('Trigger:%')
    ).order_by(Habit.confidence_score.desc()).all()
    return jsonify({"triggers": [h.to_dict() for h in habits]}), 200
