"""Inflation prediction model using machine learning"""
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_DIR, INFLATION_MODEL_FEATURES


class InflationModel:
    """
    Machine learning model to predict inflation rate based on policy parameters.
    Uses Gradient Boosting Regressor for accurate predictions.
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = INFLATION_MODEL_FEATURES
        self.is_trained = False
        
    def train(self):
        """Train the inflation prediction model on historical economic data"""
        # Load economic data
        data_path = DATA_DIR / "sample_economic_data.csv"
        df = pd.read_csv(data_path)
        
        # Create features
        df['fuel_price_change'] = df['fuel_price_index'].pct_change() * 100
        df['tax_rate_change'] = df['tax_rate'].diff()
        df['subsidy_change'] = df['subsidy_amount_billions'].pct_change() * 100
        
        # Drop NaN values from pct_change
        df = df.dropna()
        
        # Prepare features and target
        X = df[self.feature_names]
        y = df['inflation_rate']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=4,
            random_state=42
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Calculate accuracy
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        self.is_trained = True
        
        return {
            "train_score": train_score,
            "test_score": test_score,
            "feature_importance": dict(zip(
                self.feature_names,
                self.model.feature_importances_
            ))
        }
    
    def predict(self, policy_params):
        """
        Predict inflation impact based on policy parameters
        
        Args:
            policy_params (dict): Dictionary containing policy parameters
                - fuel_price_change: % change in fuel prices
                - tax_rate_change: % change in tax rate
                - subsidy_change: % change in subsidy amount
                - interest_rate: interest rate value
                - money_supply_growth: % growth in money supply
        
        Returns:
            dict: Prediction results with inflation rate and confidence
        """
        if not self.is_trained:
            self.train()
        
        # Prepare input features
        features = np.array([[
            policy_params.get('fuel_price_change', 0),
            policy_params.get('tax_rate_change', 0),
            policy_params.get('subsidy_change', 0),
            policy_params.get('interest_rate', 6.0),
            policy_params.get('money_supply_growth', 8.0)
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Predict
        inflation_rate = self.model.predict(features_scaled)[0]
        
        # Calculate confidence (based on model's prediction variance)
        # Using estimators to get prediction variance
        predictions = np.array([
            tree.predict(features_scaled)[0]
            for tree in self.model.estimators_.flatten()
        ])
        confidence = max(0, min(100, 100 - (predictions.std() * 10)))
        
        return {
            "predicted_inflation_rate": round(float(inflation_rate), 2),
            "confidence": round(float(confidence), 2),
            "baseline_inflation": 5.5,
            "change_from_baseline": round(float(inflation_rate - 5.5), 2)
        }
    
    def get_feature_importance(self):
        """Get feature importance scores"""
        if not self.is_trained:
            self.train()
        
        importance_dict = dict(zip(
            self.feature_names,
            self.model.feature_importances_
        ))
        
        # Sort by importance
        sorted_importance = sorted(
            importance_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return dict(sorted_importance)


# Singleton instance
_inflation_model_instance = None

def get_inflation_model():
    """Get or create the inflation model instance"""
    global _inflation_model_instance
    if _inflation_model_instance is None:
        _inflation_model_instance = InflationModel()
        _inflation_model_instance.train()
    return _inflation_model_instance
