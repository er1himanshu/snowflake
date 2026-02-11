"""Socio-economic risk index calculator"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import RISK_WEIGHTS


class RiskIndexModel:
    """
    Calculate composite socio-economic risk index from multiple factors.
    Risk score ranges from 0 to 100.
    """
    
    def __init__(self):
        self.weights = RISK_WEIGHTS
        self.risk_categories = {
            "Low": (0, 25),
            "Moderate": (26, 50),
            "High": (51, 75),
            "Critical": (76, 100)
        }
    
    def calculate_economic_risk(self, inflation_impact):
        """
        Calculate economic risk from inflation predictions
        
        Args:
            inflation_impact: Dict with inflation predictions
        
        Returns:
            float: Economic risk score (0-100)
        """
        inflation_rate = inflation_impact.get('predicted_inflation_rate', 5.5)
        
        # Risk increases with inflation rate
        # Baseline: 5% inflation = 30 risk
        # 10% inflation = 70 risk
        # >15% inflation = 100 risk
        
        if inflation_rate < 3:
            risk = 15
        elif inflation_rate < 5:
            risk = 25
        elif inflation_rate < 7:
            risk = 40
        elif inflation_rate < 10:
            risk = 60
        elif inflation_rate < 15:
            risk = 80
        else:
            risk = 100
        
        return float(risk)
    
    def calculate_sector_disruption_risk(self, sector_impacts):
        """
        Calculate risk from sector disruption
        
        Args:
            sector_impacts: Dict with sector impact scores
        
        Returns:
            float: Sector disruption risk (0-100)
        """
        impacts = sector_impacts.get('sector_impacts', {})
        
        # Calculate average absolute impact
        avg_abs_impact = sum(abs(v) for v in impacts.values()) / len(impacts) if impacts else 0
        
        # Calculate number of severely affected sectors (|impact| > 0.5)
        severely_affected = sum(1 for v in impacts.values() if abs(v) > 0.5)
        
        # Risk is based on severity and spread
        risk = (avg_abs_impact * 50) + (severely_affected * 8)
        
        return min(100, float(risk))
    
    def calculate_social_unrest_risk(self, sentiment_analysis):
        """
        Calculate social unrest probability risk
        
        Args:
            sentiment_analysis: Dict with sentiment analysis
        
        Returns:
            float: Social unrest risk (0-100)
        """
        unrest_prob = sentiment_analysis.get('social_unrest_probability', 0)
        negative_ratio = sentiment_analysis.get('negative_ratio', 0)
        
        # Risk based on unrest probability and negative sentiment
        risk = (unrest_prob * 70) + (negative_ratio * 0.3)
        
        return min(100, float(risk))
    
    def calculate_inequality_risk(self, policy_type, magnitude):
        """
        Estimate income inequality impact risk
        
        Args:
            policy_type: Type of policy
            magnitude: Magnitude of change
        
        Returns:
            float: Income inequality risk (0-100)
        """
        # Different policies have different inequality impacts
        inequality_factors = {
            "Fuel Price Change": 0.7,  # Regressive
            "Tax Reform": 0.5,
            "Subsidy Change": 0.8,  # Very regressive if cuts
            "Minimum Wage Change": -0.6,  # Progressive
            "Environmental Regulation": 0.4,
            "Import/Export Tariff": 0.5
        }
        
        factor = inequality_factors.get(policy_type, 0.5)
        
        # Calculate risk
        risk = abs(magnitude) * factor
        
        return min(100, max(0, float(risk)))
    
    def calculate_composite_risk(
        self,
        inflation_impact,
        sector_impacts,
        sentiment_analysis,
        policy_type,
        magnitude
    ):
        """
        Calculate composite risk index from all components
        
        Args:
            inflation_impact: Inflation prediction results
            sector_impacts: Sector impact analysis results
            sentiment_analysis: Sentiment analysis results
            policy_type: Type of policy
            magnitude: Magnitude of change
        
        Returns:
            dict: Comprehensive risk assessment
        """
        # Calculate individual risk components
        economic_risk = self.calculate_economic_risk(inflation_impact)
        sector_risk = self.calculate_sector_disruption_risk(sector_impacts)
        social_risk = self.calculate_social_unrest_risk(sentiment_analysis)
        inequality_risk = self.calculate_inequality_risk(policy_type, magnitude)
        
        # Calculate weighted composite score
        composite_score = (
            economic_risk * self.weights['economic_risk'] +
            sector_risk * self.weights['sector_disruption_risk'] +
            social_risk * self.weights['social_unrest_probability'] +
            inequality_risk * self.weights['income_inequality_impact']
        )
        
        # Determine risk level
        risk_level = None
        for level, (min_val, max_val) in self.risk_categories.items():
            if min_val <= composite_score <= max_val:
                risk_level = level
                break
        
        if risk_level is None:
            risk_level = "Critical"
        
        # Generate recommendations based on risk level
        recommendations = self._generate_recommendations(
            risk_level,
            economic_risk,
            sector_risk,
            social_risk,
            inequality_risk
        )
        
        return {
            "composite_risk_score": round(composite_score, 2),
            "risk_level": risk_level,
            "components": {
                "economic_risk": round(economic_risk, 2),
                "sector_disruption_risk": round(sector_risk, 2),
                "social_unrest_risk": round(social_risk, 2),
                "income_inequality_risk": round(inequality_risk, 2)
            },
            "recommendations": recommendations
        }
    
    def _generate_recommendations(
        self,
        risk_level,
        economic_risk,
        sector_risk,
        social_risk,
        inequality_risk
    ):
        """Generate recommendations based on risk assessment"""
        recommendations = []
        
        if risk_level == "Critical":
            recommendations.append("⚠️ CRITICAL RISK: Reconsider this policy or implement in phases")
        elif risk_level == "High":
            recommendations.append("⚠️ HIGH RISK: Implement strong mitigation measures")
        
        if economic_risk > 60:
            recommendations.append("📊 Implement monetary policy measures to control inflation")
        
        if sector_risk > 60:
            recommendations.append("🏭 Provide targeted support to heavily affected sectors")
        
        if social_risk > 60:
            recommendations.append("👥 Enhance public communication and stakeholder engagement")
        
        if inequality_risk > 60:
            recommendations.append("⚖️ Include compensatory measures for vulnerable groups")
        
        if risk_level in ["Low", "Moderate"]:
            recommendations.append("✅ Risk level acceptable with standard monitoring")
        
        return recommendations


# Singleton instance
_risk_model_instance = None

def get_risk_model():
    """Get or create the risk index model instance"""
    global _risk_model_instance
    if _risk_model_instance is None:
        _risk_model_instance = RiskIndexModel()
    return _risk_model_instance
