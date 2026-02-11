"""Sentiment analysis service"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from models.sentiment_model import get_sentiment_model


class SentimentAnalyzer:
    """Service for analyzing public sentiment"""
    
    def __init__(self):
        self.sentiment_model = get_sentiment_model()
    
    def analyze_policy_sentiment(self, policy_type, magnitude, duration_months):
        """
        Analyze public sentiment for a policy
        
        Args:
            policy_type: Type of policy change
            magnitude: Magnitude of change (%)
            duration_months: Duration of policy effect
        
        Returns:
            dict: Sentiment analysis results
        """
        result = self.sentiment_model.analyze_policy_sentiment(
            policy_type,
            magnitude,
            duration_months
        )
        
        return result
    
    def get_sentiment_summary(self, sentiment_result):
        """
        Get a human-readable sentiment summary
        
        Args:
            sentiment_result: Sentiment analysis result dict
        
        Returns:
            str: Human-readable summary
        """
        category = sentiment_result['sentiment_category']
        score = sentiment_result['overall_sentiment_score']
        negative_ratio = sentiment_result['negative_ratio']
        
        if category == "Positive":
            return f"Public sentiment is positive ({score:.2f}). Policy likely to receive support."
        elif category == "Negative":
            return f"Public sentiment is negative ({score:.2f}). {negative_ratio:.1f}% negative reactions detected."
        else:
            return f"Public sentiment is neutral ({score:.2f}). Mixed reactions expected."


# Singleton instance
_sentiment_analyzer_instance = None

def get_sentiment_analyzer():
    """Get or create the sentiment analyzer instance"""
    global _sentiment_analyzer_instance
    if _sentiment_analyzer_instance is None:
        _sentiment_analyzer_instance = SentimentAnalyzer()
    return _sentiment_analyzer_instance
