"""Tests for risk index model"""
import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from backend.models.risk_index_model import RiskIndexModel


def test_risk_model_initialization():
    """Test that model initializes correctly"""
    model = RiskIndexModel()
    assert model is not None
    assert len(model.weights) == 4
    assert sum(model.weights.values()) == 1.0  # Weights should sum to 1


def test_risk_model_economic_risk():
    """Test economic risk calculation"""
    model = RiskIndexModel()
    
    inflation_impact = {'predicted_inflation_rate': 8.5}
    risk = model.calculate_economic_risk(inflation_impact)
    
    assert 0 <= risk <= 100


def test_risk_model_sector_disruption_risk():
    """Test sector disruption risk calculation"""
    model = RiskIndexModel()
    
    sector_impacts = {
        'sector_impacts': {
            'Agriculture': -0.5,
            'Manufacturing': -0.6,
            'Services': 0.2,
            'Transport': -0.4,
            'Energy': -0.3,
            'Healthcare': 0.1,
            'Education': 0.0,
            'IT': 0.1
        }
    }
    
    risk = model.calculate_sector_disruption_risk(sector_impacts)
    
    assert 0 <= risk <= 100


def test_risk_model_composite_risk():
    """Test composite risk calculation"""
    model = RiskIndexModel()
    
    inflation_impact = {'predicted_inflation_rate': 7.5}
    sector_impacts = {
        'sector_impacts': {
            'Agriculture': -0.3,
            'Manufacturing': -0.4,
            'Services': 0.1,
            'Transport': -0.5,
            'Energy': -0.2,
            'Healthcare': 0.0,
            'Education': 0.0,
            'IT': 0.1
        }
    }
    sentiment_analysis = {
        'social_unrest_probability': 0.3,
        'negative_ratio': 45.0
    }
    
    result = model.calculate_composite_risk(
        inflation_impact,
        sector_impacts,
        sentiment_analysis,
        "Fuel Price Change",
        20
    )
    
    assert 'composite_risk_score' in result
    assert 'risk_level' in result
    assert 'components' in result
    assert 'recommendations' in result
    
    # Risk score should be between 0 and 100
    assert 0 <= result['composite_risk_score'] <= 100
    
    # Risk level should be valid
    assert result['risk_level'] in ['Low', 'Moderate', 'High', 'Critical']
    
    # Should have recommendations
    assert len(result['recommendations']) > 0


def test_risk_categories():
    """Test risk level categorization"""
    model = RiskIndexModel()
    
    # Test boundaries
    assert 'Low' in model.risk_categories
    assert 'Moderate' in model.risk_categories
    assert 'High' in model.risk_categories
    assert 'Critical' in model.risk_categories
