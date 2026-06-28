class GoalTrackingEngine:
    def __init__(self):
        pass

    def calculate_trajectory(self, target_value, time_frame, current_value, days_elapsed, total_days):
        if total_days == 0 or days_elapsed == 0:
            return {
                "required_run_rate": 0,
                "current_run_rate": 0,
                "projected_final_value": 0,
                "status": "On Track",
                "deficit": 0
            }

        current_run_rate = current_value / days_elapsed
        remaining_value = target_value - current_value
        days_remaining = total_days - days_elapsed
        
        if days_remaining > 0:
            required_run_rate = remaining_value / days_remaining
        else:
            required_run_rate = 0 if remaining_value <= 0 else remaining_value
            
        projected_final_value = current_value + (current_run_rate * days_remaining)
        deficit = target_value - projected_final_value

        if projected_final_value >= target_value:
            status = "On Track"
        elif projected_final_value >= target_value * 0.9:
            status = "At Risk"
        else:
            status = "Failing"

        return {
            "required_run_rate_per_day": required_run_rate,
            "current_run_rate_per_day": current_run_rate,
            "projected_final_value": projected_final_value,
            "status": status,
            "deficit": deficit if deficit > 0 else 0
        }
