def calculate_confidence(frequency: int, days_active: int, consistency_ratio: float, time_variance_hours: float) -> float:
    """
    Calculates a 0-100 confidence score for a detected habit.
    
    Args:
        frequency: Raw count of occurrences.
        days_active: Number of distinct days this occurred.
        consistency_ratio: How often it happens relative to active days (0.0 to 1.0).
        time_variance_hours: Standard deviation of occurrence time in hours (lower is more stable).
    """
    if frequency < 2:
        return 0.0

    # Base score driven by consistency (up to 50 points)
    consistency_score = min(50.0, consistency_ratio * 50.0)
    
    # Frequency modifier (up to 30 points)
    # 10 occurrences -> max points
    freq_score = min(30.0, (frequency / 10.0) * 30.0)
    
    # Stability modifier (up to 20 points)
    # Variance of 0 hours = 20 points, Variance > 4 hours = 0 points
    stability_score = max(0.0, 20.0 - (time_variance_hours * 5.0))
    
    total_score = consistency_score + freq_score + stability_score
    
    # Add small bonus for long-term survival
    if days_active > 14:
        total_score += 5.0
        
    return min(100.0, round(total_score, 1))
