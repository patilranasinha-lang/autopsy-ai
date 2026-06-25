# Base weights for calculating the final Productivity Score
SCORING_WEIGHTS = {
    "DEEP_WORK_WEIGHT": 0.35,
    "FOCUS_WEIGHT": 0.25,
    "CONSISTENCY_WEIGHT": 0.20,
    "DISCIPLINE_WEIGHT": 0.20
}

# Penalty coefficients
PENALTIES = {
    "CONTEXT_SWITCH": -2.0,  # Points deducted per switch beyond threshold
    "ENTERTAINMENT_PENALTY": -0.5 # Points deducted per minute over threshold
}

# Thresholds
THRESHOLDS = {
    "IDEAL_DEEP_WORK_MINUTES": 180, # 3 hours
    "ACCEPTABLE_ENTERTAINMENT_MINUTES": 60,
    "ACCEPTABLE_SWITCHES": 10
}
