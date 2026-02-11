"""Economic impact analysis service"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from models.inflation_model import get_inflation_model
from models.sector_impact_model import get_sector_model
from services.data_service import DataService


class EconomicAnalyzer:
    """Service for analyzing economic impacts of policy changes"""
    
    def __init__(self):
        self.inflation_model = get_inflation_model()
        self.sector_model = get_sector_model()
        self.data_service = DataService()
    
    def analyze_inflation_impact(self, policy_params):
        """
        Analyze inflation impact of policy
        
        Args:
            policy_params: Dict with policy parameters
        
        Returns:
            dict: Inflation impact analysis
        """
        # Get current indicators
        current_indicators = self.data_service.get_latest_economic_indicators()
        
        # Prepare model inputs
        model_params = {
            'fuel_price_change': policy_params.get('fuel_price_change', 0),
            'tax_rate_change': policy_params.get('tax_rate_change', 0),
            'subsidy_change': policy_params.get('subsidy_change', 0),
            'interest_rate': current_indicators['interest_rate'],
            'money_supply_growth': current_indicators['money_supply_growth']
        }
        
        # Get prediction
        result = self.inflation_model.predict(model_params)
        
        return result
    
    def analyze_sector_impact(self, policy_type, magnitude, affected_sectors):
        """
        Analyze sector-wise impact of policy
        
        Args:
            policy_type: Type of policy
            magnitude: Magnitude of change
            affected_sectors: List of affected sectors
        
        Returns:
            dict: Sector impact analysis
        """
        result = self.sector_model.analyze_impact(
            policy_type,
            magnitude,
            affected_sectors
        )
        
        return result
    
    def analyze_comprehensive_economic_impact(
        self,
        policy_type,
        magnitude,
        affected_sectors,
        policy_params
    ):
        """
        Comprehensive economic impact analysis
        
        Args:
            policy_type: Type of policy
            magnitude: Magnitude of change
            affected_sectors: List of affected sectors
            policy_params: Additional policy parameters
        
        Returns:
            dict: Comprehensive economic analysis
        """
        # Analyze inflation
        inflation_impact = self.analyze_inflation_impact(policy_params)
        
        # Analyze sector impacts
        sector_impact = self.analyze_sector_impact(
            policy_type,
            magnitude,
            affected_sectors
        )
        
        # Get current economic state
        current_state = self.data_service.get_latest_economic_indicators()
        
        return {
            "inflation_analysis": inflation_impact,
            "sector_analysis": sector_impact,
            "current_economic_state": current_state
        }


# Singleton instance
_economic_analyzer_instance = None

def get_economic_analyzer():
    """Get or create the economic analyzer instance"""
    global _economic_analyzer_instance
    if _economic_analyzer_instance is None:
        _economic_analyzer_instance = EconomicAnalyzer()
    return _economic_analyzer_instance
