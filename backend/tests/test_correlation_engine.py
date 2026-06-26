import pytest
from app.correlations.relationship_analyzer import RelationshipAnalyzer
from app.correlations.confidence_calculator import ConfidenceCalculator

def test_pearson_perfect_positive():
    analyzer = RelationshipAnalyzer()
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    r = analyzer.calculate_pearson(x, y)
    assert abs(r - 1.0) < 0.001

def test_pearson_perfect_negative():
    analyzer = RelationshipAnalyzer()
    x = [1, 2, 3, 4, 5]
    y = [10, 8, 6, 4, 2]
    r = analyzer.calculate_pearson(x, y)
    assert abs(r - -1.0) < 0.001

def test_pearson_no_correlation():
    analyzer = RelationshipAnalyzer()
    # Horizontal line
    x = [1, 2, 3, 4, 5]
    y = [5, 5, 5, 5, 5]
    r = analyzer.calculate_pearson(x, y)
    assert r == 0.0

def test_confidence_calculator():
    calc = ConfidenceCalculator()
    
    # Tiny sample
    assert calc.calculate(0.9, 2) == 15.0
    
    # Strong correlation, decent sample
    score_strong = calc.calculate(0.8, 20)
    assert score_strong > 80.0
    
    # Weak correlation, decent sample
    score_weak = calc.calculate(0.1, 20)
    assert score_weak < 30.0
