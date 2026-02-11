"""Core policy simulation engine"""
import sys
from pathlib import Path
from datetime import datetime
sys.path.append(str(Path(__file__).parent.parent))
from services.economic_analyzer import get_economic_analyzer
from services.sentiment_analyzer import get_sentiment_analyzer
from models.risk_index_model import get_risk_model
from config import SECTORS


class PolicySimulator:
    """
    Core orchestration engine for policy simulation.
    Coordinates all models and services to produce comprehensive analysis.
    """
    
    def __init__(self):
        self.economic_analyzer = get_economic_analyzer()
        self.sentiment_analyzer = get_sentiment_analyzer()
        self.risk_model = get_risk_model()
        self.simulation_history = []
    
    def simulate_policy(
        self,
        policy_type,
        magnitude,
        duration_months,
        affected_sectors=None,
        description=""
    ):
        """
        Run comprehensive policy simulation
        
        Args:
            policy_type: Type of policy (e.g., "Fuel Price Change")
            magnitude: Magnitude of change (%)
            duration_months: Duration of policy effect
            affected_sectors: List of sectors affected (None = all)
            description: Text description of policy
        
        Returns:
            dict: Comprehensive simulation results
        """
        if affected_sectors is None:
            affected_sectors = SECTORS
        
        # Prepare policy parameters for models
        policy_params = self._prepare_policy_params(
            policy_type,
            magnitude,
            duration_months
        )
        
        # Run economic analysis
        inflation_impact = self.economic_analyzer.analyze_inflation_impact(
            policy_params
        )
        
        sector_impact = self.economic_analyzer.analyze_sector_impact(
            policy_type,
            magnitude,
            affected_sectors
        )
        
        # Run sentiment analysis
        sentiment_analysis = self.sentiment_analyzer.analyze_policy_sentiment(
            policy_type,
            magnitude,
            duration_months
        )
        
        # Calculate risk index
        risk_assessment = self.risk_model.calculate_composite_risk(
            inflation_impact,
            sector_impact,
            sentiment_analysis,
            policy_type,
            magnitude
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            inflation_impact,
            sector_impact,
            sentiment_analysis,
            risk_assessment
        )
        
        # Compile results
        simulation_result = {
            "policy_info": {
                "type": policy_type,
                "magnitude": magnitude,
                "duration_months": duration_months,
                "affected_sectors": affected_sectors,
                "description": description,
                "timestamp": datetime.now().isoformat()
            },
            "inflation_impact": inflation_impact,
            "sector_impacts": sector_impact,
            "sentiment_analysis": sentiment_analysis,
            "risk_assessment": risk_assessment,
            "recommendations": recommendations,
            "summary": self._generate_summary(
                inflation_impact,
                sector_impact,
                sentiment_analysis,
                risk_assessment
            )
        }
        
        # Store in history
        self.simulation_history.append(simulation_result)
        
        return simulation_result
    
    def _prepare_policy_params(self, policy_type, magnitude, duration_months):
        """Prepare parameters for models based on policy type"""
        params = {
            'fuel_price_change': 0,
            'tax_rate_change': 0,
            'subsidy_change': 0
        }
        
        # Map policy type to parameters
        if policy_type == "Fuel Price Change":
            params['fuel_price_change'] = magnitude
        elif policy_type == "Tax Reform":
            params['tax_rate_change'] = magnitude / 10  # Scale down
        elif policy_type == "Subsidy Change":
            params['subsidy_change'] = magnitude
        elif policy_type == "Minimum Wage Change":
            # Affects inflation through labor costs
            params['fuel_price_change'] = magnitude * 0.3
        elif policy_type == "Environmental Regulation":
            # Affects through energy costs
            params['fuel_price_change'] = magnitude * 0.4
        elif policy_type == "Import/Export Tariff":
            # Affects through trade costs
            params['fuel_price_change'] = magnitude * 0.2
        
        return params
    
    def _generate_recommendations(
        self,
        inflation_impact,
        sector_impact,
        sentiment_analysis,
        risk_assessment
    ):
        """Generate actionable recommendations"""
        recommendations = []
        
        # Add risk-based recommendations
        recommendations.extend(risk_assessment['recommendations'])
        
        # Add sector-specific recommendations
        negative_sectors = sector_impact.get('negative_sectors', [])
        if len(negative_sectors) > 3:
            recommendations.append(
                f"🎯 Focus on supporting {', '.join(negative_sectors[:3])} sectors"
            )
        
        # Add sentiment-based recommendations
        if sentiment_analysis['negative_ratio'] > 50:
            recommendations.append(
                "📢 Strong public communication campaign needed to address concerns"
            )
        
        # Add inflation-based recommendations
        if inflation_impact['predicted_inflation_rate'] > 8:
            recommendations.append(
                "💰 Consider complementary monetary policy measures"
            )
        
        return recommendations[:6]  # Return top 6 recommendations
    
    def _generate_summary(
        self,
        inflation_impact,
        sector_impact,
        sentiment_analysis,
        risk_assessment
    ):
        """Generate executive summary"""
        inflation_rate = inflation_impact['predicted_inflation_rate']
        risk_level = risk_assessment['risk_level']
        sentiment_category = sentiment_analysis['sentiment_category']
        most_affected = sector_impact['most_affected'][:3]
        
        summary = {
            "quick_stats": {
                "inflation_rate": f"{inflation_rate}%",
                "risk_level": risk_level,
                "public_sentiment": sentiment_category,
                "most_affected_sectors": [s['sector'] for s in most_affected]
            },
            "key_findings": [
                f"Predicted inflation: {inflation_rate}% (baseline: 5.5%)",
                f"Overall risk level: {risk_level}",
                f"Public sentiment: {sentiment_category}",
                f"Most affected: {', '.join([s['sector'] for s in most_affected])}"
            ]
        }
        
        return summary
    
    def get_simulation_history(self, limit=10):
        """Get recent simulation history"""
        return self.simulation_history[-limit:]


# Singleton instance
_policy_simulator_instance = None

def get_policy_simulator():
    """Get or create the policy simulator instance"""
    global _policy_simulator_instance
    if _policy_simulator_instance is None:
        _policy_simulator_instance = PolicySimulator()
    return _policy_simulator_instance
