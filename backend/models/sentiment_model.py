"""Public sentiment analysis model using NLP"""
import json
import random
from pathlib import Path
from textblob import TextBlob
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_DIR


class SentimentModel:
    """
    Model to analyze and predict public sentiment based on policy changes.
    Uses TextBlob for sentiment analysis and generates synthetic reactions.
    """
    
    def __init__(self):
        self.sentiment_data = {}
        self._load_sentiment_data()
    
    def _load_sentiment_data(self):
        """Load sentiment templates from JSON"""
        data_path = DATA_DIR / "sample_sentiment_data.json"
        with open(data_path, 'r') as f:
            data = json.load(f)
        self.sentiment_data = data['policy_sentiments']
    
    def generate_reactions(self, policy_type, magnitude):
        """
        Generate synthetic social media reactions based on policy
        
        Args:
            policy_type: Type of policy change
            magnitude: Magnitude of change (positive or negative)
        
        Returns:
            list: Generated reaction texts
        """
        policy_data = self.sentiment_data.get(policy_type, {})
        sample_reactions = policy_data.get('sample_reactions', [
            "This policy needs careful consideration.",
            "Impact on economy remains to be seen.",
            "Government should consult experts."
        ])
        
        # Select reactions based on magnitude
        num_reactions = min(10, max(5, int(abs(magnitude) / 2)))
        reactions = random.sample(
            sample_reactions * 3,  # Repeat to have enough samples
            min(num_reactions, len(sample_reactions) * 3)
        )
        
        return reactions
    
    def analyze_sentiment(self, texts):
        """
        Analyze sentiment of text samples using TextBlob
        
        Args:
            texts: List of text strings to analyze
        
        Returns:
            dict: Sentiment analysis results
        """
        sentiments = []
        
        for text in texts:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            sentiments.append(polarity)
        
        # Calculate statistics
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        
        # Categorize sentiments
        positive_count = sum(1 for s in sentiments if s > 0.1)
        negative_count = sum(1 for s in sentiments if s < -0.1)
        neutral_count = len(sentiments) - positive_count - negative_count
        
        total = len(sentiments)
        
        return {
            "overall_sentiment_score": round(avg_sentiment, 3),
            "positive_ratio": round(positive_count / total * 100, 2) if total > 0 else 0,
            "negative_ratio": round(negative_count / total * 100, 2) if total > 0 else 0,
            "neutral_ratio": round(neutral_count / total * 100, 2) if total > 0 else 0,
            "sample_count": total
        }
    
    def extract_key_concerns(self, policy_type, magnitude):
        """
        Extract key concerns based on policy type and magnitude
        
        Args:
            policy_type: Type of policy
            magnitude: Magnitude of change
        
        Returns:
            list: Key concerns
        """
        policy_data = self.sentiment_data.get(policy_type, {})
        
        concerns = []
        
        # Add concerns based on magnitude
        if magnitude > 5:
            negative_keywords = policy_data.get('negative_keywords', [])
            concerns = random.sample(
                negative_keywords,
                min(3, len(negative_keywords))
            )
        elif magnitude < -5:
            positive_keywords = policy_data.get('positive_keywords', [])
            concerns = [f"positive: {kw}" for kw in random.sample(
                positive_keywords,
                min(2, len(positive_keywords))
            )]
        else:
            neutral_keywords = policy_data.get('neutral_keywords', [])
            concerns = random.sample(
                neutral_keywords,
                min(2, len(neutral_keywords))
            )
        
        return concerns
    
    def analyze_policy_sentiment(self, policy_type, magnitude, duration_months):
        """
        Comprehensive sentiment analysis for a policy change
        
        Args:
            policy_type: Type of policy change
            magnitude: Magnitude of change (%)
            duration_months: Duration of policy effect
        
        Returns:
            dict: Comprehensive sentiment analysis
        """
        # Generate reactions
        reactions = self.generate_reactions(policy_type, magnitude)
        
        # Analyze sentiment
        sentiment_analysis = self.analyze_sentiment(reactions)
        
        # Extract key concerns
        key_concerns = self.extract_key_concerns(policy_type, magnitude)
        
        # Calculate social unrest probability
        # Higher magnitude and negative sentiment increase unrest probability
        unrest_base = abs(magnitude) / 100 * 0.3
        sentiment_factor = max(0, -sentiment_analysis['overall_sentiment_score']) * 0.4
        duration_factor = min(duration_months / 12 * 0.2, 0.2)
        
        social_unrest_probability = min(1.0, unrest_base + sentiment_factor + duration_factor)
        
        # Determine sentiment category
        score = sentiment_analysis['overall_sentiment_score']
        if score > 0.2:
            category = "Positive"
        elif score < -0.2:
            category = "Negative"
        else:
            category = "Neutral"
        
        return {
            **sentiment_analysis,
            "sentiment_category": category,
            "key_concerns": key_concerns,
            "social_unrest_probability": round(social_unrest_probability, 3),
            "sample_reactions": reactions[:5]  # Return top 5 for display
        }


# Singleton instance
_sentiment_model_instance = None

def get_sentiment_model():
    """Get or create the sentiment model instance"""
    global _sentiment_model_instance
    if _sentiment_model_instance is None:
        _sentiment_model_instance = SentimentModel()
    return _sentiment_model_instance
