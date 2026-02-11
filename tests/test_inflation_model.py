"""Tests for inflation model"""
import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from backend.models.inflation_model import InflationModel


def test_inflation_model_initialization():
    """Test that model initializes correctly"""
    model = InflationModel()
    assert model is not None
    assert model.model is None  # Not trained yet
    assert not model.is_trained


def test_inflation_model_training():
    """Test that model can be trained"""
    model = InflationModel()
    result = model.train()
    
    assert model.is_trained
    assert model.model is not None
    assert 'train_score' in result
    assert 'test_score' in result
    assert result['train_score'] > 0


def test_inflation_model_prediction():
    """Test that model makes valid predictions"""
    model = InflationModel()
    
    policy_params = {
        'fuel_price_change': 10.0,
        'tax_rate_change': 1.0,
        'subsidy_change': -5.0,
        'interest_rate': 6.0,
        'money_supply_growth': 8.0
    }
    
    result = model.predict(policy_params)
    
    assert 'predicted_inflation_rate' in result
    assert 'confidence' in result
    assert 'baseline_inflation' in result
    
    # Inflation rate should be reasonable
    assert 0 < result['predicted_inflation_rate'] < 50
    assert 0 <= result['confidence'] <= 100


def test_inflation_model_feature_importance():
    """Test that feature importance can be retrieved"""
    model = InflationModel()
    model.train()
    
    importance = model.get_feature_importance()
    
    assert len(importance) == 5  # 5 features
    assert all(0 <= v <= 1 for v in importance.values())
