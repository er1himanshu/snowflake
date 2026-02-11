"""Tests for sentiment analyzer"""
import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from backend.models.sentiment_model import SentimentModel


def test_sentiment_model_initialization():
    """Test that model initializes correctly"""
    model = SentimentModel()
    assert model is not None
    assert len(model.sentiment_data) > 0


def test_sentiment_model_generate_reactions():
    """Test reaction generation"""
    model = SentimentModel()
    
    reactions = model.generate_reactions(
        policy_type="Fuel Price Change",
        magnitude=20
    )
    
    assert len(reactions) > 0
    assert all(isinstance(r, str) for r in reactions)


def test_sentiment_model_analyze_sentiment():
    """Test sentiment analysis"""
    model = SentimentModel()
    
    texts = [
        "This is a great policy!",
        "This is terrible and will hurt everyone.",
        "The policy is neutral."
    ]
    
    result = model.analyze_sentiment(texts)
    
    assert 'overall_sentiment_score' in result
    assert 'positive_ratio' in result
    assert 'negative_ratio' in result
    assert 'neutral_ratio' in result
    
    # Sentiment score should be between -1 and 1
    assert -1 <= result['overall_sentiment_score'] <= 1
    
    # Ratios should sum to 100
    total_ratio = (result['positive_ratio'] + 
                   result['negative_ratio'] + 
                   result['neutral_ratio'])
    assert 99 <= total_ratio <= 101  # Allow for rounding


def test_sentiment_model_analyze_policy():
    """Test comprehensive policy sentiment analysis"""
    model = SentimentModel()
    
    result = model.analyze_policy_sentiment(
        policy_type="Tax Reform",
        magnitude=15,
        duration_months=12
    )
    
    assert 'sentiment_category' in result
    assert 'key_concerns' in result
    assert 'social_unrest_probability' in result
    assert 'sample_reactions' in result
    
    # Unrest probability should be between 0 and 1
    assert 0 <= result['social_unrest_probability'] <= 1
    
    # Category should be valid
    assert result['sentiment_category'] in ['Positive', 'Negative', 'Neutral']
