from typing import List, Dict, Any
from datetime import datetime, timedelta

# pyrefly: ignore [missing-import]
from .momentum_calculator import MomentumCalculator
from .trajectory_analyzer import TrajectoryAnalyzer
from .baseline_estimator import BaselineEstimator
from .anomaly_adjuster import AnomalyAdjuster

class ProductivityForecaster:
    """
    Orchestrates the Productivity Forecasting Engine.
    Combines baseline estimations, short-term momentum, and habit trajectories
    to forecast tomorrow's productivity score.
    """
    
    def __init__(self):
        self.baseline_estimator = BaselineEstimator()
        self.momentum_calculator = MomentumCalculator()
        self.trajectory_analyzer = TrajectoryAnalyzer()
        self.anomaly_adjuster = AnomalyAdjuster()

    def forecast_tomorrow(self, user_id: int, historical_scores: List, active_habits: List) -> Dict[str, Any]:
        target_date = (datetime.utcnow() + timedelta(days=1)).date()
        
        # 1. Estimate Baseline (EMA over last 30 days)
        baseline_score = self.baseline_estimator.estimate(historical_scores)
        
        # 2. Calculate Short-Term Momentum (Last 3 days)
        momentum = self.momentum_calculator.calculate(historical_scores)
        
        # 3. Analyze Trajectory (Habit context)
        trajectory_modifier = self.trajectory_analyzer.analyze(active_habits)
        
        # 4. Combine and Adjust
        raw_forecast = baseline_score + momentum + trajectory_modifier
        final_forecast = self.anomaly_adjuster.adjust(raw_forecast, active_habits)
        
        # Cap score between 0 and 100
        final_score = max(0, min(100, final_forecast))
        
        trend = "stable"
        if final_score > baseline_score + 5:
            trend = "up"
        elif final_score < baseline_score - 5:
            trend = "down"
            
        return {
            "target_date": target_date,
            "forecasted_productivity_score": final_score,
            "forecasted_deep_work_minutes": int((final_score / 100) * 240), # rough heuristic
            "trajectory_trend": trend,
            "confidence_interval": 12.5,
            "momentum_factors": {
                "baseline": baseline_score,
                "momentum_impact": momentum,
                "habit_impact": trajectory_modifier
            }
        }
