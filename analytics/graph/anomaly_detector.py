import numpy as np

class AnomalyDetector:
    """
    Flags wildly abnormal days using Z-score thresholding.
    """
    def __init__(self, threshold=3.0):
        self.threshold = threshold

    def detect_anomalies(self, daily_scores):
        """
        Takes a list of daily productivity scores and flags anomalies.
        Returns a list of boolean flags corresponding to the input.
        """
        if not daily_scores or len(daily_scores) < 2:
            return [False] * len(daily_scores)
            
        scores = np.array(daily_scores)
        mean = np.mean(scores)
        std = np.std(scores)
        
        if std == 0:
            return [False] * len(daily_scores)
            
        z_scores = (scores - mean) / std
        anomalies = np.abs(z_scores) > self.threshold
        
        return anomalies.tolist()
