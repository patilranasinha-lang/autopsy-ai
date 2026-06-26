import pytest
from app.burnout.risk_calculator import RiskCalculator
from app.burnout.recommendation_generator import RecommendationGenerator

def test_risk_calculation():
    calc = RiskCalculator()
    
    # 0 risk across the board
    score_low, level_low = calc.calculate(0, 0, 0, 0, 0)
    assert score_low == 0.0
    assert level_low == "Low"
    
    # High workload (100) and high focus decline (100)
    # Workload = 0.30 weight -> 30
    # Decline = 0.20 weight -> 20
    # Total = 50 -> Moderate
    score_mod, level_mod = calc.calculate(100, 0, 100, 0, 0)
    assert score_mod == 50.0
    assert level_mod == "Moderate"
    
    # Max risk
    score_crit, level_crit = calc.calculate(100, 100, 100, 100, 100)
    assert score_crit == 100.0
    assert level_crit == "Critical"

def test_recommendation_generation():
    gen = RecommendationGenerator()
    
    # Test specific trigger
    rec = gen.generate(["Deep work volume is significantly higher than your baseline."])
    assert "24-hour disconnect" in rec[0]
    
    # Test fallback
    rec_empty = gen.generate([])
    assert "Maintain your current balance" in rec_empty[0]
