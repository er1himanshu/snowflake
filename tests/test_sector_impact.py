"""Tests for sector impact model"""
import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from backend.models.sector_impact_model import SectorImpactModel


def test_sector_model_initialization():
    """Test that model initializes correctly"""
    model = SectorImpactModel()
    assert model is not None
    assert len(model.sectors) == 8
    assert len(model.weights) == 8


def test_sector_model_direct_impact():
    """Test direct impact calculation"""
    model = SectorImpactModel()
    
    impact = model.calculate_direct_impact(
        policy_type="Fuel Price Change",
        magnitude=20,
        affected_sectors=["Transport", "Energy"]
    )
    
    assert len(impact) == 8
    # All impacts should be between -1 and 1
    assert all(-1 <= v <= 1 for v in impact.values())


def test_sector_model_analyze_impact():
    """Test comprehensive impact analysis"""
    model = SectorImpactModel()
    
    result = model.analyze_impact(
        policy_type="Tax Reform",
        magnitude=15,
        affected_sectors=["Manufacturing", "Services"]
    )
    
    assert 'sector_impacts' in result
    assert 'most_affected' in result
    assert 'overall_economic_impact' in result
    
    # Check impact scores are valid
    for sector, impact in result['sector_impacts'].items():
        assert -1 <= impact <= 1
    
    # Check most affected list
    assert len(result['most_affected']) <= 5


def test_sector_interdependencies():
    """Test that interdependencies are loaded"""
    model = SectorImpactModel()
    
    assert 'Energy' in model.interdependencies
    assert 'Transport' in model.interdependencies['Energy']
    
    # Dependency values should be between 0 and 1
    energy_deps = model.interdependencies['Energy']
    assert all(0 <= v <= 1 for v in energy_deps.values())
