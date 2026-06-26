from typing import Dict, Any

class InsightGenerator:
    """Generates natural language descriptions for detected habits and patterns."""
    
    def generate_routine_description(self, routine: Dict[str, Any]) -> str:
        if routine['type'] == 'time_routine':
            hour = int(routine['mean_hour'])
            ampm = "AM" if hour < 12 else "PM"
            display_hour = hour if hour <= 12 else hour - 12
            if display_hour == 0: display_hour = 12
            
            return f"User consistently engages in {routine['session_type']} around {display_hour} {ampm}."
            
        elif routine['type'] == 'day_routine':
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_name = days[routine['top_day']]
            pct = int(routine['top_day_ratio'] * 100)
            return f"{pct}% of {routine['session_type']} occurs on {day_name}."
            
        return "Detected routine pattern."

    def generate_sequence_description(self, sequence: Dict[str, Any]) -> str:
        seq_parts = sequence['sequence'].split(' -> ')
        return f"Pattern detected: {seq_parts[0]} is frequently followed by {seq_parts[1]}."
        
    def generate_trigger_description(self, trigger: Dict[str, Any]) -> str:
        if trigger['type'] == 'negative_trigger':
            return f"Warning: {trigger['trigger_event']} correlates with {trigger['impact']}."
        else:
            return f"Optimal: {trigger['trigger_event']} correlates with {trigger['impact']}."
