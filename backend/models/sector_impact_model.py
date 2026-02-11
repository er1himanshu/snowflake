"""Sector impact analysis model using input-output economic modeling"""
import json
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_DIR, SECTORS


class SectorImpactModel:
    """
    Model to calculate sector-wise economic impact of policy changes.
    Uses simplified Leontief input-output model with interdependencies.
    """
    
    def __init__(self):
        self.sectors = SECTORS
        self.weights = {}
        self.interdependencies = {}
        self._load_sector_data()
    
    def _load_sector_data(self):
        """Load sector weights and interdependencies from JSON"""
        data_path = DATA_DIR / "sector_weights.json"
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        self.weights = data['weights']
        self.interdependencies = data['interdependencies']
    
    def calculate_direct_impact(self, policy_type, magnitude, affected_sectors):
        """
        Calculate direct impact of policy on specified sectors
        
        Args:
            policy_type: Type of policy change
            magnitude: Magnitude of policy change (%)
            affected_sectors: List of directly affected sectors
        
        Returns:
            dict: Direct impact scores for each sector (-1 to 1)
        """
        direct_impacts = {}
        
        # Policy impact multipliers
        policy_multipliers = {
            "Fuel Price Change": {
                "Transport": -0.8,
                "Energy": -0.6,
                "Manufacturing": -0.5,
                "Agriculture": -0.4
            },
            "Tax Reform": {
                "Manufacturing": -0.4,
                "Services": -0.3,
                "IT": -0.3
            },
            "Subsidy Change": {
                "Agriculture": 0.6,
                "Energy": 0.4,
                "Healthcare": 0.3
            },
            "Minimum Wage Change": {
                "Services": -0.5,
                "Manufacturing": -0.4,
                "Agriculture": -0.3
            },
            "Environmental Regulation": {
                "Energy": -0.6,
                "Manufacturing": -0.5,
                "Transport": -0.4
            },
            "Import/Export Tariff": {
                "Manufacturing": 0.4,
                "IT": -0.3,
                "Services": -0.2
            }
        }
        
        # Get policy-specific multipliers
        multipliers = policy_multipliers.get(policy_type, {})
        
        # Calculate direct impact
        for sector in self.sectors:
            if sector in affected_sectors:
                base_multiplier = multipliers.get(sector, -0.3)
                impact = base_multiplier * (magnitude / 100)
                direct_impacts[sector] = max(-1, min(1, impact))
            else:
                direct_impacts[sector] = 0.0
        
        return direct_impacts
    
    def calculate_indirect_impact(self, direct_impacts):
        """
        Calculate indirect (ripple) effects across sectors using interdependencies
        
        Args:
            direct_impacts: Dictionary of direct impact scores
        
        Returns:
            dict: Indirect impact scores for each sector
        """
        indirect_impacts = {}
        
        for sector in self.sectors:
            indirect_impact = 0.0
            
            # Calculate weighted impact from all other sectors
            for other_sector in self.sectors:
                if other_sector != sector:
                    dependency = self.interdependencies[other_sector][sector]
                    direct_impact = direct_impacts[other_sector]
                    indirect_impact += dependency * direct_impact * 0.5
            
            indirect_impacts[sector] = indirect_impact
        
        return indirect_impacts
    
    def analyze_impact(self, policy_type, magnitude, affected_sectors=None):
        """
        Comprehensive sector impact analysis
        
        Args:
            policy_type: Type of policy
            magnitude: Magnitude of change (%)
            affected_sectors: List of sectors to analyze (None = all)
        
        Returns:
            dict: Comprehensive impact analysis with scores and insights
        """
        if affected_sectors is None:
            affected_sectors = self.sectors
        
        # Calculate direct impacts
        direct_impacts = self.calculate_direct_impact(
            policy_type, magnitude, affected_sectors
        )
        
        # Calculate indirect impacts
        indirect_impacts = self.calculate_indirect_impact(direct_impacts)
        
        # Combine impacts
        total_impacts = {}
        for sector in self.sectors:
            total_impact = direct_impacts[sector] + indirect_impacts[sector] * 0.6
            total_impacts[sector] = max(-1, min(1, total_impact))
        
        # Identify most affected sectors
        sorted_impacts = sorted(
            total_impacts.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        most_affected = [
            {"sector": sector, "impact": round(impact, 3)}
            for sector, impact in sorted_impacts[:5]
        ]
        
        # Calculate overall economic impact
        weighted_impact = sum(
            total_impacts[sector] * self.weights[sector]
            for sector in self.sectors
        )
        
        return {
            "sector_impacts": {
                sector: round(impact, 3)
                for sector, impact in total_impacts.items()
            },
            "most_affected": most_affected,
            "overall_economic_impact": round(weighted_impact, 3),
            "positive_sectors": [
                sector for sector, impact in total_impacts.items()
                if impact > 0.1
            ],
            "negative_sectors": [
                sector for sector, impact in total_impacts.items()
                if impact < -0.1
            ]
        }


# Singleton instance
_sector_model_instance = None

def get_sector_model():
    """Get or create the sector impact model instance"""
    global _sector_model_instance
    if _sector_model_instance is None:
        _sector_model_instance = SectorImpactModel()
    return _sector_model_instance
